import sqlite3

connection = sqlite3.connect("app.db")
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

cursor.execute("""
    INSERT INTO posts (post_title, post_author, post_content)
    VALUES (?, ?, ?)
""", ("Introduction", "Wade Smith", "Welcome to my blog!"))

cursor.execute("""
    INSERT INTO posts (post_title, post_author, post_content)
    VALUES (?, ?, ?)
""", ("My Day", "Wade Smith", "Today's a great day!"))

connection.commit()
connection.close()