"""Wallpaper changer

This is wallpaper changer, module for changing desktop background by rules
"""
__author__ = 'ales lerch'

import os
import wall
import kmeans
import database

class Editor(wall.Paper):

    def __init__(self,dir_with_imgs):
        """modules, load image to database by name,path,type as dict/obj"""
        self.directory = dir_with_imgs
        self.db = database.DB_lite()
        self.km = kmeans.Analyzer()
        super().__init__(self,dir_with_imgs)

        self.get_images()
        for img in self.img_files:
            data = {
                "name" : os.path.basename(img),
                "path" : os.path.dirname(img),
                "type" : km.check_image_color(img),
            }
            self.db.new_item(img)

    def set_timer(self):
        """ Based on time wallpaper can change"""
        pass

    def choose_image(self):
        """choose dark or light based on time"""
        pass

    def choose_random_image(self):
        """choose dark or light based on time but random"""
        pass

    def set_directory(self,directory):
        """set directory for choosing images to set as wallaper desktop,
        try to call backup direcotry if empty failed raise error"""
        self.directory = directory


