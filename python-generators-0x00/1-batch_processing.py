from seed import connect_db

def stream_users_in_batches(batch_size):
    connection = connect_db()
    if not connection:
        raise Exception("Cannot connect to the database.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM user_data')
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
    except Exception as e:
        raise Exception(e)
    finally:
        connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered = [ user for user in batch if float(user[3]) > 25]
        yield filtered

if __name__ == '__main__':
    try:
        for group in batch_processing(3):
            for user in group:
                print(user)
    except Exception as e:
        print("❌❌ sso", e)