import sqlite3

CREATE_USER_TABLE = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, score INTEGER);"
INSERT_USER = "INSERT INTO users (name, score) VALUES (?, ?);"
GET_ALL_USER = "SELECT * FROM users ORDER BY score DESC;"
GET_USER_BY_NAME ="SELECT * FROM users WHERE name = ?;"


def connect():
    return sqlite3.connect("data.db")


def create_user_table(connection):
    with connection:
        connection.execute(CREATE_USER_TABLE)


def insert_user(connection, name, score):
    with connection:
        connection.execute(INSERT_USER,(name, score,))

def get_all_user(connection):
    with connection:
        return connection.execute(GET_ALL_USER).fetchall()

def get_user_by_name(connection, name):
    with connection:
        return connection.execute(GET_USER_BY_NAME,(name,)).fetchall()