"""Wallpaper changer

This is wallpaper changer, module for changing desktop background by rules
"""
__author__ = 'ales lerch'

import os
import subprocess
from multiprocessing import active_children

try:
    from database import DB_lite, HOME
except ModuleNotFoundError:
    from .database import DB_lite, HOME

class Paper:

    def __init__(self, directory):
        self.img_files = []
        self.interrupted = False
        self.directory = directory
        self.db = DB_lite()
        self.types = (".jpg",".png",".jpeg",".tiff")

    def set_directory(self, directory):
        self.directory = directory

    def set_wallpaper(self,img):
        db_file = f"{HOME}/Library/Application Support/Dock/desktoppicture.db"
        subprocess.call(["sqlite3", db_file, f"update data set value = '{img}'"])
        subprocess.call(["killall", "Dock"])

    def set_wallpaper_with_effect(self, img, save):
        if img:
            path = f"{HOME}/Library/Application Support/WallpDesk/current/"
            cmd = b"""tell application "System Events"
        tell current desktop
            set picture rotation to 1 -- (0=off, 1=interval, 2=login, 3=sleep)
            set random order to true
            set pictures folder to alias "Macintosh HD:Users:ales:Library:Application Support:WallpDesk:current:"
            set change interval to 5.0
        end tell
    end tell"""
            subprocess.call(["mkdir","-p", path])
            subprocess.Popen(["osascript", '-'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE).communicate(cmd)

            for file_ in os.listdir(path):
                subprocess.call(["mv", f"{path}/{file_}", f"{HOME}/.Trash/"])
                if save:
                    self.save_current_wallpaper(file_)
            subprocess.call(["cp", os.path.abspath(img), path])
        else:
            print("No image found in history")

    def save_current_wallpaper(self, wallp):
        self.db.new_item("history",{"name": wallp, "path": self.directory})

    def get_images_files(self, any_ = False):
        self.img_files = []
        if self.directory:
            if self.directory and os.path.isdir(self.directory):
                for img_file in os.listdir(self.directory):
                    if os.path.splitext(img_file)[1] in self.types \
                            and img_file not in self.img_files and not any_:
                        self.img_files.append(img_file)
                    elif img_file not in self.img_files and any_:
                        self.img_files.append(img_file)
            else:
                print(f"{self.directory} folder not found")
        else:
            print("Folder for images not found")

    def shut_down(self, name):
        #in future update use mutltiprocessing.queue for sperate processes
        for process in active_children():
            if process.name == name:
                print(f"Shutting down process {process}, {process.name}, {os.getpid()}")
                process.terminate()
                process.join()

