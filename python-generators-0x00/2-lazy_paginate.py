from seed import connect_db

def paginate_users(page_size, offset):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
        return cursor.fetchall()

def lazy_paginate(page_size):
    connection = connect_db()
    if not connection:
        raise Exception("Cannot connect to database.")
    
    try:
        offset = 0
        while True:  # ✅ Only 1 loop
            page = paginate_users(page_size, offset)
            if not page:
                break
            yield page
            offset += page_size
    except Exception as e:
        raise Exception("❌ Error during pagination:", e)
    finally:
        connection.close()

if __name__ == '__main__':
    try:
        for page in lazy_paginate(2):
            for user in page:
                print(user)
            print("---- NEXT PAGE ----\n")
    except Exception as e:
        print(e)
