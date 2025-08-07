import sqlite3

conn = sqlite3.connect("app.db")
print("Connection successful!")
cursor = conn.cursor()
cursor.execute("SELECT sqlite_version();")
print("SQLite version:", cursor.fetchone())
conn.close()