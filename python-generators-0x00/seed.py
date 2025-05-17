import psycopg2
import time
import os

def connect_db():
    try:
        connection = psycopg2.connect(
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password = os.environ.get('DB_PASSWORD'),
        host = os.environ.get('DB_HOST', 'localhost'),
        port = os.environ.get('DB_PORT', 5432)
        )

        print("✅✅ Connection Successful")
        return connection
    except Exception as error:
        print("❌❌ Database connection failed.")
        return None

def create_table(connection):
    if connection:
        try:
            with connection.cursor() as curr:
                curr.execute(

                """CREATE TABLE IF NOT EXISTS user_data (
                    user_id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
                    name VARCHAR NOT NULL,
                    email VARCHAR NOT NULl UNIQUE,
                    age DECIMAL(10, 2) NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_user_data_user_id ON user_data (user_id);

                SELECT * FROM user_data;"""
                )
                print(curr.fetchone())
        except Exception as e:
            print(e)
      
        
        return
    
    print("Cannot connect to your database.")

def insert_data(connection, data):
    if not connection:
        raise Exception("Cannot connect to database")
    
    try:
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)
    """, (data['name'], data['email'], data['age']))
        connection.commit()
        cursor.close()
        print("Record created successfully")
    except Exception as e:
        raise Exception("An error occured", e)
    
if __name__ == '__main__':
    try:
        connection = connect_db()
        create_table(connection)

        insert_record = {
            'name': 'Salome Wambui',
            'email': 'salome82wambui@gmail.com',
            'age': 40
        }

        insert_data(connection, insert_record)
    except Exception as e:
        print(e)
    finally:
        connection.close()
    
