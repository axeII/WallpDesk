"""Wallpaper changer

This is wallpaper changer, module for changing desktop background by rules
"""
__author__ = 'ales lerch'

import os
import wall
import time
import sched
import random
import analyzer
import database
import datetime

class Editor(wall.Paper):

    def __init__(self,dir_with_imgs):
        """modules, load image to database by name,path,type as dict/obj"""
        self.set_timer()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.directory = dir_with_imgs
        self.db = database.DB_lite("./")
        self.km = analyzer.Kmeans()
        super().__init__(self,dir_with_imgs)

        super().get_images_files()
        for img in self.img_files:
            data = {
                "name" : os.path.basename(img),
                "path" : os.path.dirname(img),
                "type" : km.check_image_color(img),
            }
            #warning this loop can take time
            self.db.new_item(data)

    def set_timer(self, seconds = 3600):
        """ Based on time wallpaper can change"""
        self.time = seconds

    def set_directory(self,directory):
        """set directory for choosing images to set as wallaper desktop,
        try to call backup direcotry if empty failed raise error"""
        self.directory = directory

    def choose_random_image(self):
        """choose dark or light based on time but random"""
        hour = datetime.datetime.today().hour
        if hour >= 20 or (hour >= 0 and hour < 8):
            theme = "dark"
        else:
            theme = "light"

        images = self.db.get_items( type_ = theme)
        image = images[random.choice(images.keys())]
        super().set_wallpaper(f"{image[1]}/{image[2]}")

    def run(self):
            self.scheduler.enter(self.time, 1, self.choose_random_image())
            self.scheduler.run()
