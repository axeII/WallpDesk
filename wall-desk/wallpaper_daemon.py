"""Wallpaper changer

This is wallpaper changer, module for changing desktop background by rules
"""
__author__ = 'ales lerch'

import os
import time
import numpy
import random
import horizon
import analyzer
import database
from wallpaper import Wallpaper
from subprocess import Popen, PIPE
from multiprocessing import Process

class WallpaperDaemon(Wallpaper):

    def __init__(self):
        """modules, load image to database by name,path,type as dict/obj"""
        self.set_timer()
        self.db = database.DB_lite()
        check_path = self.db.get_wall_path()
        super().__init__(check_path)
        self.load_img_into_database(check_path)

    """def run_loading_images(self):
        print("starting new collection Process")
            self.process = Process(target=self.load_img_into_database, name="P_load_img_into_database", daemon=True)
            self.process.start()"""

    def set_loading_dir(self, dir_):
        self.set_directory(dir_)
        self.run_loading_images()

    def load_img_into_database(self, test_path):
        """ 
        warning loading database can now only work 
        with thread safe database no ther thread 
        can work with database at same time
        """
        assert test_path
        super().get_image_files()
        if sorted(self.img_files) != sorted(self.db.get_names()):
            print(f"[INFO] Loading images from {self.directory}")
            for image in list(filter(lambda file_: file_ not in self.db.get_names(), self.img_files)):
                data = {
                        "name" : os.path.basename(image),
                        "path" : os.path.abspath(self.directory),
                        "type" : analyzer.check_image_color(f"{os.path.abspath(self.directory)}/{image}"),
                        }
                print(f"[INFO] Adding image: {image}")
                self.db.new_item("wallpapers",data)
            print("[INFO] All images have been loaded into database")
            cmd = b"""display notification "All images are loaded to database" with title "WallpDesk" subtitle "Database synchronization" """
            Popen(["osascript", '-'], stdin=PIPE, stdout=PIPE).communicate(cmd)
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
        self.db.reset_table()
        print("starting thread to reset lb")
        self.run_loading_images()

    """def check_alive_process(self):
        return self.process.is_alive()"""

    def choose_random_image(self):
        """choose dark or light based on time but random"""
        self.sync_with_db()
        data_h = horizon.get_horizon_time(self.db.get_zone())
        if data_h["timezone"]:
            self.db.set_timezone(data_h["timezone"])
        hour, sunset, sunrise = (data_h["today_time"][0], data_h["sunset"][0], data_h["sunrise"][0])

        if hour >= sunset-2 and hour < sunset+1:
            theme = "evening"
        elif hour >= sunset or (hour >= 0 and hour < sunrise):
            theme = "dark"
        else:
            theme = "light"

        images = self.db.get_items(type_ = theme)
        #ranom.choice -> numpy.random
        image = images[random.choice(list(images.keys()))]
        print(image)
        try:
            super().set_wallpaper_with_effect(f"{image[1]}/{image[0]}", True)
        except Exception as e:
            print(e)
        cmd = f"""display notification " Chaning wallpaper to {image[0]} daemon" with title\
        "WallpDesk" subtitle "Wallpaper change theme {image[2]}" """
        Popen(["osascript", '-'], stdin=PIPE, stdout=PIPE).communicate(cmd.encode())

    """def choose_last_image(self):
        self.sync_with_db()
        img = self.db.get_last_wallpaper()
        super().set_wallpaper_with_effect(f"{img[0]}/{img[1]}", False)
        self.db.del_last_history()"""

    def changing_image(self):
        self.choose_random_image()
        while True:
            print("Running, quit application by hitting 'q'")
            time.sleep(self.time)
            self.choose_random_image()

    def run(self, alive = None):
        print(f"[INFO] Running editor with delay time: {self.time}")
        Process(target=self.changing_image, args=(),name="P_changing_image",daemon=True).start()
