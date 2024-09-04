import unittest
from src.preprocessing import preprocess_and_save
import os

class TestPreprocessing(unittest.TestCase):

    def setUp(self):
        self.image_path = 'data/raw/moon2.png'

    def test_preprocess_and_save(self):
        result_path = preprocess_and_save(self.image_path)
        self.assertTrue(os.path.exists(result_path))

if __name__ == '__main__':
    unittest.main()
