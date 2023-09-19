import sqlite3
from pysqlcipher3 import dbapi2 as sqlite

# Path to the encrypted database file
db_path = "master.db"

# Encryption key
key = "402fd482c38817c35ffa8ffb8c7d93143b749e7d315df7a81732a1ff43608497"

try:
    conn = sqlite.connect(db_path)

    conn.execute("PRAGMA cipher_compatibility = 4")
    conn.execute(f"PRAGMA key = '{key}'")
    print('got here')

    # Create a cursor
    cursor = conn.cursor()
    print('got here2')

    # Example: Print the contents of a table
    cursor.execute("SELECT * FROM djmdSongHistory")
    print('got here3')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print('got here4')

except sqlite.Error as e:
    print("SQLite error:", e)

finally:
    # Close the database connection
    conn.close()
