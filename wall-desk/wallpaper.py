"""Wallpaper changer

This is wallpaper changer, module named "Paper" for changing desktop background by rules
"""
__author__ = 'ales lerch'

import os
import re
import subprocess
import pathlib
from multiprocessing import active_children

try:
    from database import DB_lite, HOME
except ModuleNotFoundError:
    from .database import DB_lite, HOME

class Wallpaper:

    def __init__(self, directory):
        self.img_files = []
        self.interrupted = False
        self.directory = directory
        self.db = DB_lite()
        self.supported_types = [".jpg",".png",".jpeg",".tiff"]
        self.iopm = re.compile(r'IOPowerManagement.*{(.*)}')

    def set_directory(self, directory):
        self.directory = directory

    def set_wallpaper(self,img):
        db_file = f"{HOME}./walld/Dock/desktoppicture.db"
        subprocess.call(["sqlite3", db_file, f"update data set value = '{img}'"])
        subprocess.call(["killall", "Dock"])

    def set_wallpaper_with_effect(self, img, save, user="ales"):
        if img and self.get_display_status() == 4:
            path = f"{HOME}./walld/current/"
            cmd = b"""tell application "System Events"
        tell current desktop
            set picture rotation to 1 -- (0=off, 1=interval, 2=login, 3=sleep)
            set random order to true
            set pictures folder to alias "Macintosh HD:Users:{}:.walld:current:"
            set change interval to 5.0
        end tell
    end tell""".format(user)
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

    def get_file_images(self, get_all = False):
        self.img_files = []
        if self.directory and os.path.isdir(self.directory):
            for img_file in list(filter(lambda data: data not in self.img_files or get_all, os.listdir(self.directory))):
                if pathlib.Path(img_file).suffix in self.supported_types:
                    self.img_files.append(img_file)
        else:
            print(f"[ERROR] {self.directory} folder not found")

    def get_display_status(self):
        """ return iokit powermanagement status if 4 then display is on elif 1
        screen is off"""
        output = subprocess.check_output(
            'ioreg -w 0 -c IODisplayWrangler -r IODisplayWrangler'.split()).decode('utf-8')
        status = self.iopm.search(output).group(1)
        power_state = dict((k[1:-1], v) for (k, v) in
                (x.split('=') for x in status.split(',')))["CurrentPowerState"]
        return int(power_state)

    def shut_down(self, name):
        # in future update use mutltiprocessing.queue for sperate processes
        for process in active_children():
            if process.name == name:
                print(f"Shutting down process {process}, {process.name}, {os.getpid()}")
                process.terminate()
                process.join()
