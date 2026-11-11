"""Seed the demo database file used by the two login apps."""

import os
import sqlite3

from db import DEMO_USERS

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
conn.execute(
    "CREATE TABLE users ("
    "  id INTEGER PRIMARY KEY,"
    "  username TEXT UNIQUE,"
    "  password TEXT,"
    "  role TEXT"
    ")"
)
conn.executemany(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    DEMO_USERS,
)
conn.commit()
conn.close()

print(f"Created {DB_PATH} with {len(DEMO_USERS)} demo users:")
for username, _password, role in DEMO_USERS:
    print(f"  {username:<8} ({role})")
