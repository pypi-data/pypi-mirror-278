from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from src.dhuolib.config import logger


class DatabaseConnection:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.metadata = MetaData(bind=self.engine)
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def get_session(self):
        return self.Session()

    @contextmanager
    def session_scope(self, expire=False):
        session = self.get_session()
        session.expire_on_commit = expire
        try:
            yield session
            logger.info(f"Sessão foi iniciada {session}")
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Erro na sessão {session}: {e}")
            raise
        finally:
            session.close()
            logger.info(f"Sessão foi finalizada {session}")
