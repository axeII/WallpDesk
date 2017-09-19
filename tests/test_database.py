"""Test database functions."""

import unittest
from WallpDesk.database import DB_lite

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = DB_lite("tests/test_files/")
        self.db.new_item("wallpapers",{"name": 'test01',"path": 'random/paht/', "type" : 'light'})
        self.db.set_wall_path("old_path")

    def tearDown(self):
        self.db.reset_table()

    def test_get_items(self):
        """> Check output get_items"""
        result = self.db.get_items(type_ = "light")
        self.assertEqual(result[1], ['test01', 'random/paht/', 'light'])

    def test_get_one_item(self):
        """> Check result of return get_one_item"""
        result = self.db.get_one_item("test01")
        self.assertEqual(result,('test01', 'random/paht/', 'light'))

    def test_setting_wall_path(self):
        """> Check non exists image(Not found)"""
        self.db.set_wall_path("test/path/to/wall/imags")
        result = self.db.get_wall_path()
        self.assertEqual(result, "test/path/to/wall/imags")

    def test_get_wall_path(self):
        """> Check getting wall path"""
        result = self.db.get_wall_path()
        self.assertEqual(result, "old_path")

    def test_set_wall_path(self):
        """> Check settings wall path"""
        self.db.set_wall_path("new_path")
        result = self.db.get_wall_path()
        self.assertEqual(result, "new_path")

if __name__ == "__main__":
    unittest.main()
