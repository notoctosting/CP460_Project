import unittest
from scripts.data_loader import load_data

class TestDataLoader(unittest.TestCase):
    def test_load_data(self):
        data = load_data('../data/sample_data.json')
        self.assertIn("Institution_A", data)
        self.assertEqual(data["Institution_A"]["returns"], 0.05)

if __name__ == "__main__":
    unittest.main()
