# SQL Injection Lab

A hands-on teaching lab that shows exactly how SQL injection works, why it
works, and how to stop it. Built for classroom use: one vulnerable login,
one secure login, and a guided attack script, all running on Python's
standard library (SQLite) with zero dependencies.

## What students learn

- How string-built SQL queries turn user input into code
- Authentication bypass with `' OR '1'='1`
- Data extraction with `UNION SELECT`
- Why parameterized queries close the hole completely
- How to spot the same pattern in real code

## Quick start

```bash
# 1. Create the demo database
python3 lab/setup_db.py

# 2. Try a normal login (works in both apps)
python3 lab/vulnerable_app.py alice wonderland123
python3 lab/secure_app.py alice wonderland123

# 3. Run the guided attack demo
python3 lab/attack.py

# 4. Run the tests (prove the vulnerable app is exploitable
#    and the secure app is not)
python3 -m pytest tests/ -v
# or without pytest:
python3 -m unittest discover -s tests -v
```

No installation needed. Python 3.8+ only.

## Project layout

| Path | What it is |
| --- | --- |
| `lab/db.py` | Shared database setup and the two login functions |
| `lab/setup_db.py` | Seeds `lab/users.db` with demo accounts |
| `lab/vulnerable_app.py` | Login built with string-formatted SQL (the bug) |
| `lab/secure_app.py` | Same login with parameterized queries (the fix) |
| `lab/attack.py` | Guided demo: bypass + UNION extraction, side by side |
| `exercises/EXERCISES.md` | 6 student exercises with an answer key |
| `tests/test_lab.py` | Automated checks for both login functions |

## The vulnerability in one line

```python
# Vulnerable: user input becomes part of the SQL statement
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

# Secure: user input is data, never code
cursor.execute(
    "SELECT * FROM users WHERE username=? AND password=?",
    (username, password),
)
```

## Demo accounts

| Username | Password | Role |
| --- | --- | --- |
| alice | wonderland123 | student |
| bob | builder456 | student |
| admin | s3cret-admin! | administrator |

## Exercises

See `exercises/EXERCISES.md`: six exercises from "log in as admin without
the password" to "find and fix the same bug in a sample code review", with a
full answer key for the instructor.

## Safety note

This lab is for learning in a controlled environment only. The vulnerable
code here is intentionally insecure: never copy it into a real application,
and never test these payloads against systems you do not own or have explicit
permission to test.

## License

MIT. See `LICENSE`.
