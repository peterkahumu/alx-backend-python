import psycopg2

def connect_to_db(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT):
    
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
