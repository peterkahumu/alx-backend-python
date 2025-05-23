import psycopg2
import os
from datetime import datetime
from db_connection import connect_to_db

def log_queries(func):
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else '')
        print(f"[Log]: Executing SQL query: {query} at {datetime.now().time()}")
        return func(*args, **kwargs)    
    return wrapper

@log_queries
def fetch_all_users(query):
    connection = None
    try:
        connection = connect_to_db(
            DB_NAME= os.environ.get("DB_NAME"),
            DB_USER = os.environ.get("DB_USER"),
            DB_PASSWORD = os.environ.get("DB_PASSWORD"),
            DB_HOST = os.environ.get("DB_HOST", "localhost"),
            DB_PORT = os.environ.get("DB_PORT", 5432)
        )

        if not connection:
            raise RuntimeError("Cannot Connect to your Database")
        
        cursor = connection.cursor()
        cursor.execute(query=query)
        for row in cursor.fetchall():
            yield row
    except Exception as e:
        raise Exception(e)
    finally:
        if connection:
            connection.close()
            print('[log]: Connection closed')


if __name__ == '__main__':
    users = fetch_all_users("SELECT * FROM user_data")
    for user in users:
        print(user)
    