from db_connection import with_db_connection
from time import sleep

def retry_on_fail(retries=3, delay=1):
    def decorator(func):
        def wrapper(connection, *args, **kwargs):
            if not connection:
                raise RuntimeError("Cannot connect to your database.")
            
            counter = 1
            while counter <= retries:
                try:
                    return func(connection, *args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}. Retrying {counter}/{retries}...")
                    counter += 1
                    sleep(delay)
            raise Exception(f"Failed after {retries} attempts.")
        return wrapper
    return decorator

@with_db_connection
@retry_on_fail(retries=2, delay=2)
def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)

if __name__ == '__main__':
    execute_query("SELECT * FROM use_data")


    