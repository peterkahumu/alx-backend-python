from seed import connect_db

def stream_users(connection, limit):
    if not connection:
        raise Exception("Cannot connect to the database.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM user_data LIMIT {limit}")
            while True:
                user = cursor.fetchone()
                if user is None:
                    break
                yield user
    except Exception as e:
        raise Exception(e)
    

if __name__ == '__main__':
    try:
        connection = connect_db()
        users = stream_users(connection,3)

        for user in users:
            print(user)
            print()
    except Exception as e:
        print(e)
    