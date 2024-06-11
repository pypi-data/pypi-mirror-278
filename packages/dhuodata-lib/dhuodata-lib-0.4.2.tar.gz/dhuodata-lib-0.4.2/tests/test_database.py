import unittest
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
# Adjust this import according to your project structure
from dhuolib.repository import DatabaseConnection, GenericRepository
from sqlalchemy import text
import pandas as pd


class TestDatabaseConnection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config_file_name = 'tests/files/database.json'
        cls.db_connection = DatabaseConnection(config_file_name=cls.config_file_name)

    def test_database_connection_init(self):
        db_connection = DatabaseConnection(self.config_file_name)
        self.assertIsNotNone(db_connection.engine)
        self.assertIsNotNone(db_connection.session)

    def test_session_scope(self):
        with self.db_connection.session_scope() as session:
            self.assertIsNotNone(session)


class TestGenericRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config_file_name = 'tests/files/database.json'
        cls.db_connection = DatabaseConnection(config_file_name=cls.config_file_name)
        cls.table_name = 'test_table'
        cls.repo = GenericRepository(db_connection=cls.db_connection)
        cls.repo.db.session.execute(text(
            f"CREATE TABLE IF NOT EXISTS {cls.table_name} (id INTEGER PRIMARY KEY, name VARCHAR(255), age INTEGER, predict VARCHAR(255), version VARCHAR(255), created_at TIMESTAMP)"))

    @classmethod
    def tearDownClass(cls):
        with cls.db_connection.session_scope() as session:
            session.execute(text(f"DROP TABLE IF EXISTS {cls.table_name}"))

    def setUp(self):
        self.db_connection = self.__class__.db_connection
        self.repo = self.__class__.repo
        self.table_name = self.__class__.table_name

    def tearDown(self):
        with self.db_connection.session_scope() as session:
            session.execute(text(f"DELETE FROM {self.table_name}"))

    def test_1_insert(self):
        data = {'id': 1, 'name': 'John Doe', 'age': 30}
        inserted = self.repo.insert(self.table_name, data)
        with self.repo.db.session_scope() as session:
            result = session.execute(
                text(f"SELECT * FROM {self.table_name} WHERE id=1")).fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result.name, 'John Doe')
            self.assertEqual(result.age, 30)
            self.assertEqual(inserted.name, 'John Doe')
            self.assertEqual(inserted.age, 30)

    def test_2_get_items_with_pagination(self):
        for i in range(10):
            data = {'id': i + 1, 'name': f'User {i+1}', 'age': 20 + i}
            self.repo.insert(self.table_name, data)

        items = self.repo.get_items_with_pagination(self.table_name, 1, 5)
        self.assertEqual(len(items["items"]), 5)
        self.assertEqual(items["items"][0].name, 'User 1')
        self.assertEqual(items["items"][4].name, 'User 5')

        items = self.repo.get_items_with_pagination(self.table_name, 2, 5)
        self.assertEqual(len(items["items"]), 5)
        self.assertEqual(items["items"][0].name, 'User 6')
        self.assertEqual(items["items"][4].name, 'User 10')

    def test_3_update(self):
        data = {'id': 1, 'name': 'John Doe', 'age': 30, 'predict': 'Negative'}
        self.repo.insert(table_name=self.table_name, data=data)

        updated_data = {'id': 1, 'name': 'John Doe', 'age': 30, 'predict': 'Positive'}
        self.repo.update(
            table_name=self.table_name, index=updated_data['id'], predict=updated_data['predict'])

        with self.repo.db.session_scope() as session:
            result = session.execute(
                text(f"SELECT * FROM {self.table_name} WHERE id={int(updated_data['id'])}")).fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result.predict, 'Positive')
            self.assertEqual(result.name, 'John Doe')

    def test_4_insert_invalid_data(self):
        invalid_data = {'id': 1, 'invalid_column': 'Invalid Data'}
        with self.assertRaises(Exception):
            self.repo.insert(self.table_name, invalid_data)

    def test_5_update_table_by_dataframe(self):
        initial_data = pd.DataFrame([
            {'id': 1, 'name': 'John Doe', 'age': 30, 'predict': 'Positive'}
        ])
        self.repo.update_table_by_dataframe(
            table_name=self.table_name, df_predict=initial_data, if_exists='replace')

        new_data = pd.DataFrame([
            {'id': 2, 'name': 'Jane Doe', 'age': 25, 'predict': 'Positive', 'version': 1, 'created_at': '2021-01-01'},
            {'id': 3, 'name': 'Jim Beam', 'age': 35, 'predict': 'Negative', 'version': 1, 'created_at': '2021-01-01'}
        ])
        self.repo.update_table_by_dataframe(self.table_name, new_data)

        df = self.repo.to_dataframe(self.table_name)
        self.assertEqual(len(df), 3)
        self.assertListEqual(list(df['name']), ['John Doe', 'Jane Doe', 'Jim Beam'])
        self.assertListEqual(list(df['predict']), ['Positive', 'Positive', 'Negative'])
