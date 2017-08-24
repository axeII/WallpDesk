"""Database

Database model for comunicating with database
"""
__author__ = 'ales lerch'

import sqlite3
import subprocess

class DB_lite:

    def __init__(self,path_to_db = "~/Library/Application Support/Pydesktop/"):
        try:
            self.db = sqlite3.connect(f"{path_to_db}pydesktop.db")
        except Exception:
            print("[Error] Database not found creating database")
            subprocess.call(["touch", f"{path_to_db}pydesktop.db"])
            self.db = sqlite3.connect(f"{path_to_db}pydesktop.db")

        try:
            self.cursor = self.db.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS wallpapers(id INTEGER PRIMARY KEY, name TEXT uniuqe,
                                   path TEXT, type TEXT)
            """)
            self.db.commit()
        except Exception as excpt:
            self.db.rollback()
            raise excpt
        finally:
            self.db.close()

    def new_item(self,data):
        if data:
            try:
                self.cursor.execute("""INSERT INTO wallpapers(name, path, type)
                                  VALUES({data["name"]},{data["path"]},{data["type"]})""")
                self.db.commit()
            except sqlite3.IntegrityError:
                print('[Error] Record already exists')

    def get_items(self, type_ = ""):
        data_items = {}
        if type_:
            cursor.execute(f"""SELECT id, name, path, type FROM wallpapers WHERE type={type_}""")
        else:
            cursor.execute("""SELECT id, name, path, type FROM wallpapers""")
        for row in cursor:
            # row[0] returns the first column in the query
            data_items[row[0]] = [row[1],row[2],row[3]]
        return data_items

    def get_one_item(self,which_one):
        self.cursor.execute('''SELECT name, path, type FROM wallpapers WHERE name=?''', (which_one,))
        return self.cursor.fetchone()

    def update_item_path(self,value, name):
        self.cursor.execute('''UPDATE wallpapers SET path = ? WHERE name = ? ''',
            (value, name))
        self.db.commit()

    def del_item(self, item_name):
        self.cursor.execute("""DELETE FROM wallpapers WHERE name = ? """,
            (item_name))
        self.db.commit()

    def reset_db(self):
        self.cursor.execute("""DROP TABLE IF EXISTS wallpapers""")
        self.db.commit()

    def __exit__(self):
        self.db.close()
