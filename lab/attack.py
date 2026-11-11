"""Guided attack demo: the same payloads against both login functions.

Run: python3 lab/attack.py

Shows, side by side, how classic SQL injection payloads break the
vulnerable login and bounce off the secure one.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from db import create_connection, secure_login, vulnerable_login

PAYLOADS = [
    ("Normal login (alice)", "alice", "wonderland123"),
    ("Auth bypass: ' OR '1'='1", "admin", "' OR '1'='1"),
    ("Auth bypass as admin: admin' --", "admin' --", "anything"),
    ("UNION extraction", "' UNION SELECT 1, username, password FROM users --", "x"),
    ("Wrong password (control)", "alice", "wrong-password"),
]


def run_demo(login_fn, label):
    print(f"\n--- {label} ---")
    conn = create_connection()
    for name, username, password in PAYLOADS:
        try:
            user = login_fn(conn, username, password)
        except Exception as exc:  # noqa: BLE001 - show DB errors to the student
            print(f"  {name:<38} -> ERROR: {exc}")
            continue
        if user:
            print(f"  {name:<38} -> LOGGED IN as {user[1]} ({user[2]})")
        else:
            print(f"  {name:<38} -> rejected")
    conn.close()


def main():
    print("SQL Injection Lab: guided attack demo")
    print("Same payloads, two login functions. Watch what changes.")
    run_demo(vulnerable_login, "VULNERABLE login (string-formatted SQL)")
    run_demo(secure_login, "SECURE login (parameterized queries)")
    print(
        "\nTakeaway: the payloads did not change. The code did.\n"
        "Parameterized queries keep user input as data, never as code."
    )


if __name__ == "__main__":
    main()
