"""Tests for the SQL Injection Lab.

They prove two things:
1. The vulnerable login really is exploitable (bypass + UNION extraction).
2. The secure login resists the same payloads while still accepting
   legitimate credentials.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lab"))

from db import create_connection, secure_login, vulnerable_login  # noqa: E402


class TestLogins(unittest.TestCase):
    def setUp(self):
        self.conn = create_connection()

    def tearDown(self):
        self.conn.close()

    def test_legitimate_login_works_in_both(self):
        for login in (vulnerable_login, secure_login):
            user = login(self.conn, "alice", "wonderland123")
            self.assertIsNotNone(user)
            self.assertEqual(user[1], "alice")
            self.assertEqual(user[2], "student")

    def test_wrong_password_rejected_by_both(self):
        for login in (vulnerable_login, secure_login):
            self.assertIsNone(login(self.conn, "alice", "wrong-password"))

    def test_auth_bypass_works_on_vulnerable_only(self):
        # ' OR '1'='1 makes the WHERE clause true for every row, so the
        # first user in the table is returned.
        user = vulnerable_login(self.conn, "admin", "' OR '1'='1")
        self.assertIsNotNone(user)
        self.assertIsNone(secure_login(self.conn, "admin", "' OR '1'='1"))

    def test_comment_bypass_logs_in_as_admin_on_vulnerable_only(self):
        # admin' -- comments out the password check entirely.
        user = vulnerable_login(self.conn, "admin' --", "anything")
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "admin")
        self.assertEqual(user[2], "administrator")
        self.assertIsNone(secure_login(self.conn, "admin' --", "anything"))

    def test_comment_bypass_works_on_vulnerable_only(self):
        user = vulnerable_login(self.conn, "' OR 1=1 --", "anything")
        self.assertIsNotNone(user)
        self.assertIsNone(secure_login(self.conn, "' OR 1=1 --", "anything"))

    def test_union_extraction_works_on_vulnerable_only(self):
        payload = "' UNION SELECT 1, username, password FROM users --"
        user = vulnerable_login(self.conn, payload, "x")
        # UNION sorts the combined rows, so the admin row comes first.
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "admin")
        self.assertEqual(user[2], "s3cret-admin!")
        self.assertIsNone(secure_login(self.conn, payload, "x"))

    def test_secure_login_treats_payload_as_literal_username(self):
        # The payload is just a weird username that matches nobody.
        self.assertIsNone(
            secure_login(self.conn, "' OR '1'='1", "' OR '1'='1")
        )


if __name__ == "__main__":
    unittest.main()
