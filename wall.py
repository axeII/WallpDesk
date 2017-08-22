"""Wallpaper changer

This is wallpaper changer, module for changing desktop background by rules
"""
__author__ = 'ales lerch'

import os

class Paper:

    def __init__(self,directory):
        self.img_files = []
        self.directory = directory
        self.types = (".jpg",".png",".jpeg",".tiff")

    def set_wallpaper(self,img):
        db_file = "~/Library/Application Support/Dock/desktoppicture.db"
        subprocess.call(["sqlite3", db_file, f"update data set value = '{img}'"])
        subprocess.call(["killall", "Dock"])

    def get_images_files(self):
        if self.directory:
            for img_file in os.listdir(self.directory):
                if img_file.splitext[1] in self.types:
                    self.img_files.append(img_file)

