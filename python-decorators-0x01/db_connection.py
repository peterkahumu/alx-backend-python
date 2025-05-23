import psycopg2
import os
from datetime import datetime

def connect_to_db(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT):
    
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        connection = connect_to_db(
            os.environ.get('DB_NAME'),
            os.environ.get('DB_USER'),
            os.environ.get('DB_PASSWORD'),
            os.environ.get('DB_HOST', 'localhost'),
            os.environ.get('DB_PORT', 5432)
        )
        print(f'[Log]: Database Connection initaited at: {datetime.now().time()}')

        query = kwargs.get('query') or (args[0] if args else '')
        try:
            print(f'[Log]: Executing SQL query: {query}')
            result = func(connection, *args, **kwargs)
            return result
        finally:
            connection.close()
            print("[log]: Database Connection closed.")

    return wrapper

