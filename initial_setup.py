import sqlite3

conn = sqlite3.connect('users.db')

cur = conn.cursor()

cur.execute("""CREATE TABLE users(
        username text,
        email_address text,
        salt text,
        hash text
);""")