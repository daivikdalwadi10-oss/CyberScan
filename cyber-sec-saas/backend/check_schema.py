import sqlite3

conn = sqlite3.connect('cybersec.db')
cursor = conn.cursor()

# Get CREATE TABLE for users
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
result = cursor.fetchone()
if result:
    print("Users table schema:")
    print(result[0])
    print("\n" + "="*60)
    
    # Get columns
    cursor.execute("PRAGMA table_info(users)")
    cols = cursor.fetchall()
    print("\nColumns:")
    for col in cols:
        print(f"  {col[1]:30} {col[2]}")
else:
    print("Users table not found")
    
# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print("\n\nAll tables:")
for table in tables:
    print(f"  - {table[0]}")

conn.close()
