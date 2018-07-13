"""Wallpaper changer

This is wallpaper changer, module named "Paper" for changing desktop background by rules
"""
__author__ = 'ales lerch'

import os
import re
import pathlib
from multiprocessing import active_children
from subprocess import call, check_output, PIPE, Popen

try:
    from database import DB_lite, HOME
except ModuleNotFoundError:
    from .database import DB_lite, HOME

class Wallpaper:

    def __init__(self, directory):
        self.img_files = []
        self.all_files = []
        self.db = DB_lite()
        self.interrupted = False
        self.directory = directory
        self.iopm = re.compile(r'IOPowerManagement.*{(.*)}')
        self.supported_types = [".jpg",".png",".jpeg",".tiff"]

    def set_directory(self, directory):
        self.directory = directory

    def set_wallpaper(self,img):
        db_file = f"{HOME}/.walld/Dock/desktoppicture.db"
        call(["sqlite3", db_file, f"update data set value = '{img}'"])
        call(["killall", "Dock"])

    def set_wallpaper_with_effect(self, img, save, user="ales"):
        """
        warning osascript currently broken use set_wallpaper
        without any effect until issue will be fixed
        or set manualy
        or find other solution
        """
        if img and self.get_display_status() == 4:
            path = f"{HOME}/.walld/current/"
            os.makedirs(path, exist_ok=True)
            cmd = f"""tell application "System Events"
            tell current desktop
                set picture rotation to 1 -- (0=off, 1=interval, 2=login, 3=sleep)
                set random order to true
                set pictures folder to alias "Macintosh HD:Users:{user}:.walld:current:"
                set change interval to 5.0
            end tell
        end tell"""
            #Popen(["osascript", '-'], stdin=PIPE, stdout=PIPE).communicate(cmd.encode())
            for file_ in os.listdir(path):
                call(["mv", f"{path}/{file_}", f"{HOME}/.Trash/"])
                if save:
                    self.save_current_wallpaper(file_)
            call(["cp", os.path.abspath(img), path])
        else:
            print("No image found in history")

    def save_current_wallpaper(self, wallp):
        self.db.new_item("history",{"name": wallp, "path": self.directory})

    def get_image_files(self):
        self.img_files = []
        if self.directory and os.path.isdir(self.directory):
            for img_file in list(filter(lambda data: data not in self.img_files or get_all, os.listdir(self.directory))):
                if pathlib.Path(img_file).suffix in self.supported_types:
                    self.img_files.append(img_file)
        else:
            print(f"[ERROR] {self.directory} folder not found")

    def get_all_files(self):
        self.all_files = []
        for found_file in os.listdir(self.directory):
            self.all_files.append(found_file)

    def get_display_status(self):
        """
        return iokit powermanagement status if 4 then display is on 
        else 1 screen is off
        """
        output = check_output(
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
