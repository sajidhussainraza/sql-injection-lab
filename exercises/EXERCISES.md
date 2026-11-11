# Student Exercises

Work through these in order. Everything runs locally on the demo database;
nothing touches a real system.

## Exercise 1: Log in normally

Run `python3 lab/setup_db.py`, then log in as `alice` with password
`wonderland123` using both apps. Confirm both accept the login.

## Exercise 2: Log in as admin without the password

Using only the vulnerable app, log in as `admin` without knowing the
password `s3cret-admin!`. Hint: the password field is part of the SQL
query, and `--` comments out the rest of a line. What happens if your
username is `admin' --`?

Bonus: try password `' OR '1'='1` with username `admin`. You get in, but
as which user, and why?

## Exercise 3: Explain the query

Write out the full SQL statement the vulnerable app builds when you enter
username `admin` and password `' OR '1'='1`. Mark which part is the
developer's intended logic and which part is the attacker's injected logic.

## Exercise 4: Steal the password list

Use a `UNION SELECT` payload in the username field to make the vulnerable
app return usernames and passwords. What does the query return, and why
does the number of selected columns matter?

## Exercise 5: Try the same attacks on the secure app

Run every payload from Exercises 2 and 4 against `secure_app.py`.
Record the result for each one and explain in one sentence why it fails.

## Exercise 6: Code review

A colleague shows you this code and asks if it is safe:

```python
cursor.execute(
    "SELECT * FROM users WHERE username='%s'" % username
)
```

Is it safe? Rewrite it the secure way, then write a one-paragraph note to
your colleague explaining the change.

---

## Answer key (instructors)

**Exercise 1:** Both apps print `Login successful! Welcome, alice (student).`

**Exercise 2:** `python3 lab/vulnerable_app.py "admin' --" anything` logs in
as admin. The query becomes
`... WHERE username='admin' --' AND password='anything'`, and everything
after `--` is a comment, so the password is never checked. Bonus: password
`' OR '1'='1` also gets you in, but as `alice`, the first row in the table,
because `OR '1'='1'` makes the WHERE clause true for every user and the app
takes the first match.

**Exercise 3:** Full query for username `admin` and password `' OR '1'='1`:
`SELECT id, username, role FROM users WHERE username='admin' AND password='' OR '1'='1'`.
Intended logic: `username='admin' AND password=''`. Injected logic:
`OR '1'='1'`, which turns the whole WHERE clause true.

**Exercise 4:** Username `' UNION SELECT 1, username, password FROM users --`
makes the query return every user's credentials (the `--` comments out the
rest of the query). The app shows the first row, which is admin's
credentials. The UNION must select the same number of columns as the original
query (3: id, username, role), so the payload selects `1, username, password`.

**Exercise 5:** Every payload is rejected by the secure app. The `?`
placeholders send the payload to the database as a literal string value,
so it is compared against stored usernames instead of being executed.

**Exercise 6:** Not safe: `%` string formatting pastes input into the SQL
just like an f-string. Secure version:
`cursor.execute("SELECT * FROM users WHERE username=?", (username,))`.
