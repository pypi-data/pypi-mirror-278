import unittest
import os
from src.session_manager import SessionManager
from src.logger import Logger

class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.session_manager = SessionManager(self.logger)

    def test_save_load_session(self):
        session_name = "test_session"
        prompt = "Create a Python function to add two numbers"
        generated_code = "def add(a, b):\n    return a + b"
        self.session_manager.save_session(session_name, prompt, generated_code)
        loaded_session = self.session_manager.load_session(session_name)
        self.assertEqual(loaded_session["prompt"], prompt)
        self.assertEqual(loaded_session["generated_code"], generated_code)
        os.remove(f"sessions/{session_name}.json")

if __name__ == "__main__":
    unittest.main()
