import unittest
import os
from src.code_storage import CodeStorage
from src.logger import Logger

class TestCodeStorage(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.code_storage = CodeStorage(self.logger)

    def test_save_code(self):
        file_name = "test_code.py"
        code = "def add(a, b):\n    return a + b"
        self.code_storage.save_code(file_name, code)
        with open(file_name, "r") as f:
            saved_code = f.read()
        self.assertEqual(saved_code, code)
        os.remove(file_name)

if __name__ == "__main__":
    unittest.main()
