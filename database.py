import logging
import psycopg2
from psycopg2 import Error
from psycopg2.errors import UniqueViolation
from config import DB_HOST, DB_USER, DB_PORT, DB_PASSWORD, CREATE_DB, CREATE_TABLES, DB_NAME
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

logging.basicConfig(level=logging.DEBUG)


class Database:
    """Class for work with database"""
    def __init__(self):
        self._conn = self.connection()
        logging.info('Connection established')
        self.create_db()
        self._conn = self.connection(DB_NAME)
        self.create_tables()

    def update_tables(self):
        update_tables_query = "ALTER TABLE users_words ADD CONSTRAINT unique_all_fields UNIQUE (user_id, word_id);"
        self._execute_query(update_tables_query)

    def insert_user(self, user_id: int):
        insert_query = f"INSERT INTO users (user_id) VALUES ({user_id});"
        try:
            self._execute_query(insert_query)
        except UniqueViolation:
            logging.info('This user already exists')

    def insert_word(self, word: str, meaning: str):
        try:
            insert_query = f"INSERT INTO words (word, meaning) VALUES ('{word}', '{meaning}');"
            self._execute_query(insert_query)
        except UniqueViolation:
            logging.info(f'This word {word} is already exist')

    def update_user_words(self, user_id: int, word: str, feature: str):
        update_query = f"INSERT INTO users_words (user_id, word_id, feature) VALUES ({user_id}, " \
                       f"(SELECT word_id FROM words WHERE word = '{word}'), '{feature}') " \
                       f"ON CONFLICT ON CONSTRAINT unique_all_fields DO UPDATE " \
                       f"SET user_id = {user_id}, " \
                       f"word_id = (SELECT word_id FROM words WHERE word = '{word}'), " \
                       f"feature = '{feature}';"
        self._execute_query(update_query)

    def delete_user(self, user_id: int):
        delete_query = f"DELETE FROM users WHERE user_id = {user_id};"
        self._execute_query(delete_query)

    def create_db(self):
        db_exists = self._execute_query(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname='{DB_NAME}';", True)
        if not db_exists:
            self._execute_query(CREATE_DB)
            logging.info(f'Database {DB_NAME} created')

    def create_tables(self):
        tables_exists = self._execute_query(
            f"SELECT to_regclass('public.users');", True)[0]
        logging.info(f'Tables are exist? {bool(tables_exists)}')
        if not tables_exists:
            self._execute_query(CREATE_TABLES)
            logging.info('Tables created')

    def _execute_query(self, query, select=False):
        cursor = self._conn.cursor()
        cursor.execute(query)
        if select:
            records = cursor.fetchone()
            cursor.close()
            return records
        else:
            self._conn.commit()
        cursor.close()

    def connection(self, database=None):
        try:
            if not database:
                conn = psycopg2.connect(user=DB_USER,
                                        password=DB_PASSWORD,
                                        host=DB_HOST,
                                        port=DB_PORT)
            else:
                conn = psycopg2.connect(user=DB_USER,
                                        password=DB_PASSWORD,
                                        host=DB_HOST,
                                        port=DB_PORT,
                                        database=database)
                logging.info(f'Connected to Database {DB_NAME}')
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            return conn
        except (Exception, Error) as error:
            logging.error(error)
            return None
