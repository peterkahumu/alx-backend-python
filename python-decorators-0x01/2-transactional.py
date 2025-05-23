import psycopg2
from db_connection import connect_to_db
import os

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        connection = connect_to_db(
            os.environ.get('DB_NAME'),
            os.environ.get('DB_USER'),
            os.environ.get('DB_PASSWORD'),
            os.environ.get('DB_HOST', 'localhost'),
            os.environ.get('DB_PORT', 5432)
        )

        try:
            result = func(connection, *args, **kwargs)
            return result
        finally:
            connection.close()
            print("[log]: Database Connection closed.")

    return wrapper


def transactional(func):
    def wrapper(connection, *args, **kwargs):
        try:
            print('[log]: The connection is as follows:', connection)
            result = func(connection, *args, **kwargs)
            print('[Log]: Transaction has completed and commited.')
            connection.commit()
            return result
        except Exception as e:
            connection.rollback()
            print('[Log]: Transaction failed miserably 🤣🤣')
            raise e
        
    return wrapper

@with_db_connection
@transactional
def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)


if __name__ == '__main__':
    execute_query("SELECT * FROM user_data")