"""Secure login app. Same login, fixed with parameterized queries.

Usage:
    python3 lab/secure_app.py <username> <password>

Example:
    python3 lab/secure_app.py alice wonderland123
    python3 lab/secure_app.py admin "' OR '1'='1"   # fails, as it should
"""

import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(__file__))

from db import secure_login

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def main(argv):
    if len(argv) != 3:
        print("Usage: python3 secure_app.py <username> <password>")
        return 2
    if not os.path.exists(DB_PATH):
        print("Database not found. Run: python3 lab/setup_db.py")
        return 1

    conn = sqlite3.connect(DB_PATH)
    user = secure_login(conn, argv[1], argv[2])
    conn.close()

    if user:
        print(f"Login successful! Welcome, {user[1]} ({user[2]}).")
        return 0
    print("Login failed: invalid username or password.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
