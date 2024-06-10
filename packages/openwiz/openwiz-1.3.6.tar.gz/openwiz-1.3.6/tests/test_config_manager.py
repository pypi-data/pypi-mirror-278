import unittest
import yaml
from src.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.config_manager = ConfigManager()

    def test_load_config(self):
        config = self.config_manager.load_config()
        self.assertIn("api_key", config)

if __name__ == "__main__":
    unittest.main()
