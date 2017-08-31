"""Test analyzer functions."""

import unittest
from WallpDesk import analyzer

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        pass

    def test_check_image_color(self):
        """> Check image for color(light)"""
        result = analyzer.check_image_color("tests/test_files/sample.jpg")
        self.assertEqual(result, "light")

    def test_check_wrong_image(self):
        """> Check non exists image(Not found)"""
        result = analyzer.check_image_color("tests/test_files/non_exists.jpg")
        self.assertEqual(result, "Image not found")

if __name__ == "__main__":
    unittest.main()
