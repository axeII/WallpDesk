"""Wallpaper changer

This is wallpaper changer, module for changing desktop background by rules
"""
__author__ = 'ales lerch'

import os
import wall
import time
import random
import analyzer
import database
import datetime
import threading
from queue import Queue

class Editor(wall.Paper):

    def __init__(self,dir_with_imgs):
        """modules, load image to database by name,path,type as dict/obj"""
        self.set_timer()
        self.db = database.DB_lite()
        self.directory = dir_with_imgs
        self.que = Queue(maxsize = 1)
        self.que.put(threading.Thread(target=self.loop))
        super().__init__(dir_with_imgs)

        self.load_thread = threading.Thread(target=self.load_img_database)
        self.load_thread.start()

    def set_loading_dir(self, dir_):
        if not self.load_thread.isAlive():
            print('starting thread')
            self.set_directory(dir_)
            threading.Thread(target=self.load_img_database).start()

    def load_img_database(self):
        """ warning loading database can now only work 
        with thread safe database no ther thread can work with database"""
        super().get_images_files()
        if sorted(self.img_files) != sorted(self.db.get_names()):
            print("loading images...")
            for img in self.img_files:
                data = {
                    "name" : os.path.basename(img),
                    "path" : os.path.abspath(self.directory),
                    "type" : analyzer.check_image_color(
                        f"{os.path.abspath(self.directory)}/{img}"),
                }
                self.db.new_item(data)
            print("all images loaded to databse")
        print("Database with images set!")

    def set_timer(self, seconds = 3600):
        """ Based on time wallpaper can change"""
        self.time = seconds

    def set_directory(self,directory):
        """set directory for choosing images to set as wallaper desktop,
        try to call backup direcotry if empty failed raise error"""
        self.directory = directory

    def sync_with_db(self):
        for local_file in os.listdir(self.directory):
            if local_file not in self.img_files:
                self.img_files.append(local_file)

        for db_file in self.db.get_names():
            if db_file not in os.listdir(self.directory):
                self.db.del_item(db_file)
        print("Synced with database")

    def reset_library(self):
        self.db.clean_table()

    def choose_random_image(self):
        """choose dark or light based on time but random"""
        self.sync_with_db()
        hour = datetime.datetime.today().hour
        if hour >= 20 or (hour >= 0 and hour < 8):
            theme = "dark"
        else:
            theme = "light"

        if not self.load_thread.isAlive():
            images = self.db.get_items(type_ = theme)
            image = images[random.choice(list(images.keys()))]
            super().set_wallpaper(f"{image[1]}/{image[0]}")

    def run(self):
        if self.que.empty():
            self.que.put(threading.Thread(target=self.loop))
        self.que.get().start()

    def loop(self):
        while True:
            time.sleep(self.time)
            if self.interrupted:
                break
            self.choose_random_image()

if __name__ == "__main__":
    e = Editor("./testimg")
