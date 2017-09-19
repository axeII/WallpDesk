"""Wallpaper changer

This is wallpaper changer, module for changing desktop background by rules
"""
__author__ = 'ales lerch'

import os
import wall
import time
import random
import horizon
import analyzer
import database
from subprocess import Popen, PIPE
from multiprocessing import Process


class Editor(wall.Paper):

    def __init__(self):
        """modules, load image to database by name,path,type as dict/obj"""
        self.set_timer()
        self.db = database.DB_lite()
        self.process = Process(target=self.load_img_database, name="P_load_img_database", daemon=True)
        check_path = self.db.get_wall_path()
        super().__init__(check_path)
        if check_path:
            self.process.start()

    def run_loading_images(self):
        #should I kill process for another loading?
        if not self.process.is_alive():
            print("starting new collection Process")
            self.process = Process(target=self.load_img_database, name="P_load_img_database", daemon=True)
            self.process.start()

    def set_loading_dir(self, dir_):
        self.set_directory(dir_)
        self.run_loading_images()

    def load_img_database(self):
        """ warning loading database can now only work 
        with thread safe database no ther thread can work with database"""
        super().get_images_files()
        if sorted(self.img_files) != sorted(self.db.get_names()):
            print("loading images...")
            for img in self.img_files:
                if img in self.db.get_names():
                    continue
                data = {
                    "name" : os.path.basename(img),
                    "path" : os.path.abspath(self.directory),
                    "type" : analyzer.check_image_color(
                        f"{os.path.abspath(self.directory)}/{img}"),
                }
                print(f"ading: {img}")
                self.db.new_item("wallpapers",data)
            print("all images loaded to databse")
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

        if not self.process.is_alive():
            images = self.db.get_items(type_ = theme)
            image = images[random.choice(list(images.keys()))]
            print(image)
            super().set_wallpaper_with_effect(f"{image[1]}/{image[0]}", True)
            cmd = f"""display notification " Chaning wallpaper to {image} daemon" with title\
            "WallpDesk" subtitle "Wallpaper change" """
            Popen(["osascript", '-'], stdin=PIPE, stdout=PIPE).communicate(cmd.encode())

    def choose_last_image(self):
        self.sync_with_db()
        if not self.process.is_alive():
            img = self.db.get_last_wallpaper()
            super().set_wallpaper_with_effect(f"{img[0]}/{img[1]}", False)
            self.db.del_last_history()

    def changing_image(self):
        while True:
            time.sleep(self.time)
            self.choose_random_image()

    def run(self):
        print(f"runing editorh with time: {self.time}")
        Process(target=self.changing_image,name="P_changing_image",daemon=True).start()

