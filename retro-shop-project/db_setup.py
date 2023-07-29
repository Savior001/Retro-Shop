import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Thelegendofzelda1!',
            database='retro_shop'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()

        # Replace the table columns with your desired column names and data types.
        # For example, 'id' can be an auto-incrementing primary key, 'name' can be VARCHAR, 'price' can be FLOAT, etc.
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS retro_shop (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price FLOAT NOT NULL,
                quantity_available INT NOT NULL
            )
        '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'retro_shop' created successfully.")
    except Error as e:
        print(f"Error: {e}")

def main():
    connection = create_connection()
    if connection is not None:
        create_table(connection)
        connection.close()

if __name__ == '__main__':
    main()
