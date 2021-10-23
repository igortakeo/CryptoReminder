import sqlite3

conn = sqlite3.connect('cryptobot.db')

''''
conn.execute("""
  CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    username TEXT NOT NULL UNIQUE
  )
""")
'''

conn.commit()
conn.close()