import sqlite3

connection = sqlite3.connect('app.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
post_id INTEGER PRIMARY KEY,
post_title TEXT,
post_date TEXT DEFAULT CURRENT_TIMESTAMP,
post_author TEXT,
post_content TEXT
)
""")

connection.commit()
connection.close()