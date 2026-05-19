import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from model.db import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_connect(self):
        conn = self.db.connect()
        self.assertIsNotNone(conn)

    def test_execute(self):
        cursor = self.db.execute("CREATE TABLE IF NOT EXISTS test_table (id INTEGER)")
        self.assertIsNotNone(cursor)

    def test_query(self):
        result = self.db.query("SELECT 1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 1)

    def test_query_one(self):
        result = self.db.query_one("SELECT 1")
        self.assertEqual(result[0], 1)

    def test_close(self):
        self.db.close()
        self.assertIsNone(self.db.connection)


if __name__ == "__main__":
    unittest.main()