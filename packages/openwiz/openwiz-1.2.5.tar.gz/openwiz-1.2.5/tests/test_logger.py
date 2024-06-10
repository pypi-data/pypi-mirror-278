import unittest
import logging
from src.logger import Logger

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()

    def test_log(self):
        self.logger.log("Test log message")
        with open("app.log", "r") as f:
            log_content = f.read()
        self.assertIn("Test log message", log_content)

if __name__ == "__main__":
    unittest.main()
