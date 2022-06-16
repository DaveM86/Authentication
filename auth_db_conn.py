import sqlite3

def set_connection():
    return sqlite3.connect('users.db')
