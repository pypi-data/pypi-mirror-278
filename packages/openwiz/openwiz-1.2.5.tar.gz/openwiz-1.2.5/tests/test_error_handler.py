import unittest
from src.error_handler import ErrorHandler
from src.logger import Logger

class TestErrorHandler(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.error_handler = ErrorHandler(self.logger)

    def test_handle(self):
        try:
            raise ValueError("Test error")
        except ValueError as e:
            self.error_handler.handle(e)
            with open("app.log", "r") as f:
                log_content = f.read()
            self.assertIn("Test error", log_content)

if __name__ == "__main__":
    unittest.main()
