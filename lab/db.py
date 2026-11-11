"""Shared database helpers for the SQL Injection Lab.

Everything here uses only the Python standard library (sqlite3).

The two login functions are the heart of the lab:

- vulnerable_login() builds SQL by pasting user input into the query
  string. That is the bug students exploit.
- secure_login() passes user input as parameters. The database treats
  them as data, never as code, so the same payloads fail.
"""

import sqlite3

DEMO_USERS = [
    ("alice", "wonderland123", "student"),
    ("bob", "builder456", "student"),
    ("admin", "s3cret-admin!", "administrator"),
]


def create_connection(db_path=":memory:"):
    """Return a SQLite connection with the demo schema and seed data."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "  id INTEGER PRIMARY KEY,"
        "  username TEXT UNIQUE,"
        "  password TEXT,"
        "  role TEXT"
        ")"
    )
    conn.executemany(
        "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
        DEMO_USERS,
    )
    conn.commit()
    return conn


def vulnerable_login(conn, username, password):
    """Log in using string-formatted SQL. DO NOT USE IN REAL CODE.

    The query is built by pasting the inputs straight into the SQL text,
    so a crafted username can change the meaning of the query itself.
    Returns the matched user row, or None.
    """
    query = (
        "SELECT id, username, role FROM users "
        f"WHERE username='{username}' AND password='{password}'"
    )
    cursor = conn.execute(query)
    return cursor.fetchone()


def secure_login(conn, username, password):
    """Log in using parameterized queries. This is the correct pattern.

    The ? placeholders keep user input as data. Even a classic injection
    payload is treated as a literal username that matches nobody.
    Returns the matched user row, or None.
    """
    cursor = conn.execute(
        "SELECT id, username, role FROM users "
        "WHERE username=? AND password=?",
        (username, password),
    )
    return cursor.fetchone()
