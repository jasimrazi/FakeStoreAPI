import sqlite3

# Path to your SQLite database file
db_path = 'db.sqlite3'  # Adjust the path as necessary

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check and print all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:", [table[0] for table in tables])

    # Query to check the structure of the user_login table
    cursor.execute("PRAGMA table_info(user_login);")
    columns = cursor.fetchall()

    # Print the columns information
    for column in columns:
        print(f"Column Name: {column[1]}, Data Type: {column[2]}")

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
finally:
    # Close the connection if it was successfully opened
    if conn:
        conn.close()
