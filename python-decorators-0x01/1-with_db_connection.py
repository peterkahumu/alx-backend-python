from db_connection import connect_to_db
import os
from datetime import datetime

def open_and_close_db(func):
    def wrapper(*args, **kwargs):
        connection = kwargs.get('connection') or (args[0] if args else '')
        query = kwargs.get('query') or (args[1] if args else '')
        if not connection:
            raise RuntimeError("Please provide a database connection object as the first argument or use the keyword =>  'connection = ...'")
        if not query:
            raise RuntimeError("Please provide a query as the second argument or use the keyword => 'query=...'")
        print(f"[log]: Executing sql query: {query}. Start time = {datetime.now().time()}")
        try:
            yield from func (*args, **kwargs)
        finally:
            print(f"[Log]: Closing the database connection @{datetime.now().time()}")
            connection.close()
    return wrapper

@open_and_close_db
def fetch_all_users(connection: object, query: str, limit:int = None):
    try:
        count=0
        cursor = connection.cursor()
        cursor.execute(query)
        for user in cursor.fetchall():
            if limit and count >=limit:
                break
            yield user
            count+=1
    except Exception as error:
        raise Exception("Could not fetch users", error)


if __name__ == "__main__":
    connection = connect_to_db(
        os.environ.get('DB_NAME'),
        os.environ.get('DB_USER'),
        os.environ.get('DB_PASSWORD'),
        os.environ.get('DB_HOST', 'localhost'),
        os.environ.get('DB_PORT', 5432)
    )

    users = fetch_all_users(connection, "SELECT * FROM user_data LIMIT 5")
    for user in users:
        print(user)
