from seed import connect_db

def stream_users():
    connection = connect_db()
    correct_limit = False

    while not correct_limit:
        try:
            limit = int(input("Please enter the number of users you want to print : "))
            correct_limit = True
        except Exception as e:
            print(f"Invalid input, {e}")

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
        
        users = stream_users()

        for user in users:
            print(user)
            print()
    except Exception as e:
        print(e)
    