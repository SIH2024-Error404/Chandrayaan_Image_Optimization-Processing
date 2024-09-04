import unittest
from src.preprocessing import reduce_noise, adjust_contrast
import cv2

class TestPreprocessing(unittest.TestCase):

    def setUp(self):
        self.image = cv2.imread('data/raw/moon2.png')

    def test_reduce_noise(self):
        result = reduce_noise(self.image)
        self.assertIsNotNone(result)

    def test_adjust_contrast(self):
        result = adjust_contrast(self.image)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
