import mysql.connector

# Connect to MySQL
try:
    # Connection info
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="hive",
        port=9999
    )

    if db_connection.is_connected():
        print("Connection Success")

        cursor = db_connection.cursor()

        cursor.execute("SELECT * FROM Persons")

        rows = cursor.fetchall()

        for row in rows:
            print(row)

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # Close cursor
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'db_connection' in locals() and db_connection.is_connected():
        db_connection.close()
        print("db connection shutdown..")
