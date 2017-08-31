"""Test analyzer functions."""

import unittest
from WallpDesk import analyzer

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        pass

    def test_check_image_color(self):
        result = analyzer.check_image_color("tests/test_files/sample.jpg")
        self.assertEqual(result, "light")

if __name__ == "__main__":
    unittest.main()
