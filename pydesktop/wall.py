"""Wallpaper changer

This is wallpaper changer, module for changing desktop background by rules
"""
__author__ = 'ales lerch'

import os
import subprocess

class Paper:

    def __init__(self,directory):
        self.img_files = []
        self.directory = directory
        self.types = (".jpg",".png",".jpeg",".tiff")

    def set_wallpaper(self,img):
        db_file = "~/Library/Application Support/Dock/desktoppicture.db"
        subprocess.call(["sqlite3", db_file, f"update data set value = '{img}'"])
        subprocess.call(["killall", "Dock"])

    def set_wallpaper_with_effect(self, img):
        path = "~/Library/Application Support/Pydesk/current"
        cmd = """tell application "System Events"
                 tell current desktop
                 set picture rotation to 1 -- (0=off, 1=interval, 2=login, 3=sleep)
                 set random order to true
                 set pictures folder to file "Users:ales:Library:Application Support:current:"
                 set change interval to 5.0
                 end tell
                end tell"""
        subprocess.Popen(["osascript", '-'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE).communicate(cmd)

        for file_ in os.listdir(path):
            subprocess.call(["mv", os.path.abspath(file_), "~/.Trash/"])
        subprocess.call(["mv", os.path.abspath(img), path])

    def get_current_wallpaper(self):
       pass

    def get_images_files(self):
        if self.directory:
            for img_file in os.listdir(self.directory):
                if img_file.splitext[1] in self.types:
                    self.img_files.append(img_file)
