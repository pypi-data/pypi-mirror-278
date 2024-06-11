import json
import sys
import pandas as pd

from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

from dhuolib.config import logger


class DatabaseConnection:
    def __init__(self, config_file_name=None):
        if self.in_dataflow():
            self.connection_string = f"oracle+oracledb://{sys.argv[1]}"
        else:
            f = open(config_file_name)
            data = json.load(f)
            self.connection_string = data["connection_string"]

        self.engine = self._get_engine(self.connection_string)
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def in_dataflow(self):
        if str(Path.home()) == "/home/dataflow":
            return True
        return False

    def _get_engine(self, connection_string):
        self.engine = create_engine(connection_string)
        return self.engine

    @contextmanager
    def session_scope(self, expire=False):
        self.session.expire_on_commit = expire
        try:
            yield self.session
            logger.info(f"Sessão foi iniciada {self.session}")
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"Erro na sessão {self.session}: {e}")
            raise
        finally:
            self.session.close()
            logger.info(f"Sessão foi finalizada {self.session}")


class GenericRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def insert(self, table_name: str, data: dict):
        with self.db.session_scope() as session:
            columns = ", ".join(data.keys())
            values = ", ".join([f":{key}" for key in data.keys()])
            query = text(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
            session.execute(query, data)
            inserted_predict = session.execute(
                text(
                    f"SELECT * FROM {table_name} WHERE id = (SELECT MAX(id) FROM {table_name})"
                )
            ).fetchone()
        return inserted_predict

    # replace_or_append tabela na base de dados
    def update_table_by_dataframe(
        self, table_name: str, df_predict: pd.DataFrame, if_exists: str = "append"
    ):
        with self.db.session_scope() as session:
            df = pd.read_sql(f"SELECT VERSION FROM {table_name}", con=session.bind)
            latest_version = df["version"].max()
            if pd.isna(latest_version):
                latest_version = 1
            else:
                latest_version = int(latest_version) + 1

            df_predict["version"] = latest_version
            df_predict["created_at"] = datetime.now()

            df_predict["created_at"] = pd.to_datetime(df_predict["created_at"])
            df_predict.to_sql(
                name=table_name, con=session.bind, if_exists=if_exists, index=False
            )

    def get_items_with_pagination(
        self, table_name: str, page: int = 1, page_size: int = 10000
    ):
        offset = (page - 1) * page_size
        items = []
        with self.db.session_scope() as session:
            query = text(
                f"SELECT * FROM {table_name} ORDER BY id LIMIT :limit OFFSET :offset"
            )
            items = session.execute(
                query, {"offset": offset, "limit": page_size}
            ).fetchall()

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": len(items),
        }

    def to_dataframe(
        self,
        table_name: str = None,
        filter_clause: str = None,
        list_columns: list = None,
    ):
        columns = ""
        df = None
        query = ""

        if list_columns:
            columns = ", ".join([column for column in list_columns])
        else:
            columns = "*"

        if filter_clause:
            query = f"SELECT {columns} FROM {table_name} WHERE {filter_clause}"
        else:
            query = f"SELECT {columns} FROM {table_name}"

        with self.db.session_scope() as session:
            df = pd.read_sql(query, con=session.bind)
        return df

    def get_by_id(self, table_name: str, id: int):
        with self.db.session_scope() as session:
            query = text(f"SELECT * FROM {table_name} WHERE id = :id")
            item = session.execute(query, {"id": id}).fetchone()
        return item

    def get_all(self, table_name: str):
        with self.db.session_scope() as session:
            query = text(f"SELECT * FROM {table_name}")
            items = session.execute(query).fetchall()
        return items

    def update(self, table_name: str, index: int, predict: str):
        with self.db.session_scope() as session:
            update_query = text(
                f"UPDATE {table_name} SET predict = :predict WHERE id = :id"
            )
            session.execute(
                update_query, {"id": int(index), "predict": predict}
            )
            updated_predict = session.execute(
                text(
                    f"SELECT * FROM {table_name} WHERE id = (SELECT MAX(id) FROM {table_name})"
                )
            ).fetchone()
        return updated_predict
