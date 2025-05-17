from seed import connect_db

def stream_user_ages():
    connection = connect_db()
    if not connection:
        raise Exception("Cannot connect to database.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT age FROM user_data")
            while True:  # ✅ 1st loop
                row = cursor.fetchone()
                if row is None:
                    break
                yield float(row[0])
    except Exception as e:
        raise Exception("❌ Error streaming ages:", e)
    finally:
        connection.close()

def calculate_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():  # ✅ 2nd loop
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        print(f"Average age of users: {total_age / count:.2f}")

if __name__ == '__main__':
    calculate_average_age()
