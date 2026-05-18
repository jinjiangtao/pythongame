
import unittest
import os
from src.db import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    TEST_DB_NAME = "test_notes.db"

    def setUp(self):
        if os.path.exists(self.TEST_DB_NAME):
            os.remove(self.TEST_DB_NAME)
        self.db = DatabaseManager(self.TEST_DB_NAME)

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.TEST_DB_NAME):
            os.remove(self.TEST_DB_NAME)

    def test_add_note(self):
        note_id = self.db.add_note("Test Title", "Test Content")
        self.assertIsNotNone(note_id)
        self.assertGreater(note_id, 0)

    def test_get_note_by_id(self):
        note_id = self.db.add_note("Test Title", "Test Content")
        note = self.db.get_note_by_id(note_id)
        self.assertIsNotNone(note)
        self.assertEqual(note[1], "Test Title")
        self.assertEqual(note[2], "Test Content")

    def test_get_all_notes(self):
        self.db.add_note("Title 1", "Content 1")
        self.db.add_note("Title 2", "Content 2")
        notes = self.db.get_all_notes()
        self.assertEqual(len(notes), 2)

    def test_update_note(self):
        note_id = self.db.add_note("Old Title", "Old Content")
        success = self.db.update_note(note_id, "New Title", "New Content")
        self.assertTrue(success)
        note = self.db.get_note_by_id(note_id)
        self.assertEqual(note[1], "New Title")
        self.assertEqual(note[2], "New Content")

    def test_delete_note(self):
        note_id = self.db.add_note("Test Title", "Test Content")
        success = self.db.delete_note(note_id)
        self.assertTrue(success)
        note = self.db.get_note_by_id(note_id)
        self.assertIsNone(note)

if __name__ == "__main__":
    unittest.main()
