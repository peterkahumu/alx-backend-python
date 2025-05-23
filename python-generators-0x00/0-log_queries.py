import psycopg2
import os
from datetime import datetime

def log_queries(func):
    def wrapper(*args, **kwargs):
        query = query = kwargs.get('query') or (args[0] if args else '')
        print(f"[Log]: Executing SQL query: {query} at {datetime.now().time()}")
        return func(*args, **kwargs)    
    return wrapper

def open_close_database(func):
    def wrapper(*args, **kwargs):
        connection = kwargs.get('connection') or (args[0] if args else '')
        if not connection:
            raise Exception("The wrapper cannot locate the connection to the database.")
        
        func(*args, **kwargs)

        connection.close()

@log_queries
def fetch_all_users(query):
    try:
        connection = psycopg2.connect(
            dbname = os.environ.get("DB_NAME"),
            user = os.environ.get("DB_USER"),
            password = os.environ.get("DB_PASSWORD"),
            host = os.environ.get("DB_HOST", "localhost"),
            port = os.environ.get("DB_PORT", 5432)
        )

        if not connection:
            raise RuntimeError("Cannot Connect to your Database")
        
        cursor = connection.cursor()
        cursor.execute(query=query)
        results = cursor.fetchall()
        connection.close()
        yield results

    except Exception as e:
        raise Exception(e)


if __name__ == '__main__':
    fetch_all_users("SELECT * FROM user_data")

    