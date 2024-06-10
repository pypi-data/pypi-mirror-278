import unittest
from src.api_client import APIClient
from src.logger import Logger

class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.api_client = APIClient("test_api_key", self.logger)

    def test_generate_code(self):
        prompt = "Create a Python function to add two numbers"
        generated_code = self.api_client.generate_code(prompt)
        self.assertIn("def", generated_code)

if __name__ == "__main__":
    unittest.main()
