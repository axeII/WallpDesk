"""Test wall functions."""

import unittest
from WallpDesk.wall import Paper

class TestWall(unittest.TestCase):

    def setUp(self):
        self.wall = Paper("tests/test_files/")

    def test_get_images_correct(self):
        """> Check image for color(light)"""
        self.wall.get_images_files()
        self.assertEqual(self.wall.img_files, ["sample.jpg"])

    def test_get_images_wrong(self):
        """> Check non exists image(Not found)"""
        self.wall.set_directory("tests/none_exist/folder")
        self.wall.get_images_files()
        self.assertEqual(self.wall.img_files, [])

if __name__ == "__main__":
    unittest.main()
