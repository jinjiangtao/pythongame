
import unittest
import os
from src.note_core import NoteCore
from src.db import DatabaseManager

class TestNoteCore(unittest.TestCase):
    TEST_DB_NAME = "test_notes.db"

    def setUp(self):
        if os.path.exists(self.TEST_DB_NAME):
            os.remove(self.TEST_DB_NAME)
        self.db_manager = DatabaseManager(self.TEST_DB_NAME)
        self.note_core = NoteCore(self.db_manager)

    def tearDown(self):
        self.db_manager.close()
        if os.path.exists(self.TEST_DB_NAME):
            os.remove(self.TEST_DB_NAME)

    def test_save_new_note(self):
        success = self.note_core.save_note("Test Title", "Test Content")
        self.assertTrue(success)
        self.assertIsNotNone(self.note_core.current_note_id)

    def test_save_note_empty_content(self):
        with self.assertRaises(ValueError):
            self.note_core.save_note("Test Title", "")
        with self.assertRaises(ValueError):
            self.note_core.save_note("", "Test Content")
        with self.assertRaises(ValueError):
            self.note_core.save_note("   ", "   ")

    def test_update_note(self):
        self.note_core.save_note("Old Title", "Old Content")
        note_id = self.note_core.current_note_id
        success = self.note_core.save_note("New Title", "New Content")
        self.assertTrue(success)
        self.assertEqual(self.note_core.current_note_id, note_id)
        note = self.db_manager.get_note_by_id(note_id)
        self.assertEqual(note[1], "New Title")
        self.assertEqual(note[2], "New Content")

    def test_load_note(self):
        self.note_core.save_note("Test Title", "Test Content")
        note_id = self.note_core.current_note_id
        self.note_core.create_new_note()
        self.assertIsNone(self.note_core.current_note_id)
        note = self.note_core.load_note(note_id)
        self.assertIsNotNone(note)
        self.assertEqual(self.note_core.current_note_id, note_id)

    def test_delete_note(self):
        self.note_core.save_note("Test Title", "Test Content")
        note_id = self.note_core.current_note_id
        success = self.note_core.delete_note(note_id)
        self.assertTrue(success)
        self.assertIsNone(self.note_core.current_note_id)
        note = self.db_manager.get_note_by_id(note_id)
        self.assertIsNone(note)

    def test_get_all_notes(self):
        self.note_core.save_note("Title 1", "Content 1")
        self.note_core.create_new_note()
        self.note_core.save_note("Title 2", "Content 2")
        notes = self.note_core.get_all_notes()
        self.assertEqual(len(notes), 2)

if __name__ == "__main__":
    unittest.main()
