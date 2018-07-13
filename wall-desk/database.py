"""Database

Database model for comunicating with database
"""
__author__ = "ales lerch"

import os
import sqlite3
import subprocess

HOME = os.getenv("HOME")


class DB_lite:
    def __init__(self, path_to_db=f"{HOME}/.walld/"):
        try:
            self.db = sqlite3.connect(
                f"{path_to_db}pydesktop.db", check_same_thread=False
            )
        except Exception:
            print("[Error] Database not found creating database")
            subprocess.call(["mkdir", "-p", f"{path_to_db}"])
            subprocess.call(["touch", f"{path_to_db}pydesktop.db"])
            self.db = sqlite3.connect(
                f"{path_to_db}pydesktop.db", check_same_thread=False
            )

        try:
            self.cursor = self.db.cursor()
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS wallpapers(id INTEGER PRIMARY KEY, name TEXT uniuqe,
                                   path TEXT, type TEXT)
            """
            )
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY, path TEXT, name TEXT)
            """
            )
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS settings(id INTEGER PRIMARY KEY, set_path TEXT)
            """
            )
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS timezone(id INTEGER PRIMARY KEY, zone TEXT)
            """
            )
            self.db.commit()
        except Exception as excpt:
            self.db.rollback()
            print("closing database")
            self.db.close()
            raise excpt

    def new_item(self, table, data):
        if data and table:
            try:
                if table == "wallpapers":
                    self.cursor.execute(
                        f"""INSERT INTO wallpapers(name, path, type)
                                      VALUES("{data["name"]}","{data["path"]}","{data["type"]}")"""
                    )
                elif table == "history":
                    self.cursor.execute(
                        f"""INSERT INTO history(path, name)
                                      VALUES("{data["name"]}", "{data["path"]}")"""
                    )
                self.db.commit()
            except sqlite3.IntegrityError:
                print("[Error] Record already exists")

    def set_wall_path(self, in_path):
        self.cursor.execute(
            f"""REPLACE INTO settings(id, set_path) VALUES (1,"{in_path}")"""
        )
        self.db.commit()

    def set_timezone(self, zone):
        self.cursor.execute(f"""REPLACE INTO timezone(id, zone) VALUES(1, "{zone}")""")
        self.db.commit()

    def get_names(self):
        ret = []
        self.cursor.execute("""SELECT id, name, path, type FROM wallpapers""")
        for row in self.cursor:
            ret.append(row[1])
        return ret

    def get_one_item(self, which_one):
        self.cursor.execute(
            """SELECT name, path, type FROM wallpapers WHERE name=?""", (which_one,)
        )
        return self.cursor.fetchone()

    def get_last_wallpaper(self):
        self.cursor.execute(
            """SELECT name, path FROM history WHERE id=(SELECT MAX(id) FROM history)"""
        )
        return self.cursor.fetchone()

    def get_wall_path(self):
        self.cursor.execute("""SELECT * FROM settings WHERE id=1""")
        try:
            return self.cursor.fetchone()[1]
        except:
            return None

    def get_zone(self):
        self.cursor.execute("""SELECT * FROM timezone WHERE id=1""")
        try:
            return self.cursor.fetchone()[1]
        except:
            return None

    def get_items(self, type_=""):
        data_items = {}
        if type_:
            self.cursor.execute("""SELECT * FROM wallpapers WHERE type=? """, (type_,))
        else:
            self.cursor.execute("""SELECT id, name, path, type FROM wallpapers""")
        for row in self.cursor:
            data_items[row[0]] = [row[1], row[2], row[3]]
        return data_items

    def update_item_path(self, value, name):
        self.cursor.execute(
            """UPDATE wallpapers SET path = ? WHERE name = ? """, (value, name)
        )
        self.db.commit()

    def del_item(self, item_name):
        self.cursor.execute(f"""DELETE FROM wallpapers WHERE name = "{item_name}" """)
        self.db.commit()

    def del_last_history(self):
        self.cursor.execute(
            """DELETE FROM history WHERE id=(SELECT MAX(id) FROM history)"""
        )
        self.db.commit()

    def delete_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS wallpapers""")
        self.db.commit()

    def reset_table(self):
        self.cursor.execute("""DELETE FROM wallpapers""")
        self.cursor.execute("""DELETE FROM settings""")
        self.db.commit()

    def __exit__(self):
        self.db.close()
