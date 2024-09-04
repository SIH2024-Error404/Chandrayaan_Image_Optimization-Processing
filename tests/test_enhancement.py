import unittest
from src.enhancement import enhance_image
import cv2

class TestEnhancement(unittest.TestCase):

    def setUp(self):
        self.image = cv2.imread('data/raw/moon2.png')

    def test_enhance_image(self):
        result = enhance_image(self.image)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
