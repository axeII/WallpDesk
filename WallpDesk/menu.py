"""Menu_bar

Menu bar module for setting menu bar setup for OSX
"""
__author__ = 'ales lerch'

import rumps
import desktop
import wallpaper
import tkinter as tk
from wall import HOME
from os.path import isfile
from tkinter import filedialog

class Bar(rumps.App):

    def __init__(self):
        super(Bar, self).__init__("WallpDesk")
        self.menu = ["About","Settings", None,
                "Desktop daemon", "Wallpaper damon", None
                ,"Next wallpaper", "Quit"]
        #self.def_desktop = f"{HOME}/Desktop/" should be always desktop duh
        self.def_wallpaper = f"{HOME}/TimeDayWall/"
        self.quit_button = None
        self.template = True
        self.title = None
        if isfile("images/menu_bar.png"):
            self.icon = "images/menu_bar.png"
        else:
            self.title = "Icon not found"

        self.root = tk.Tk()
        self.root.withdraw()
        self.editor = wallpaper.Editor(self.def_wallpaper)
        self.desktop = desktop.Daemon()

    @rumps.clicked("About")
    def about(self, _):
        pass

    @rumps.clicked("Settings")
    def settings(self, _):
        file_path = filedialog.askdirectory()
        if self.def_wallpaper != file_path:
            self.def_wallpaper = file_path
            print(self.def_wallpaper)
            self.editor.set_loading_dir(self.def_wallpaper)

    @rumps.clicked("Desktop daemon")
    def on_off_test(self, sender):
        """ notifications are so far broken in rumps
        rumps.notification(title='Hi', subtitle='There.', message='Friend!',
        sound=does_something.sound, data=my_data)"""
        sender.state = not sender.state
        if sender.state:
            rumps.alert(message='You are now running desktop daemon')
            self.desktop.interrupted = False
            self.desktop.run()
        else:
            self.desktop.interrupted = True

    @rumps.clicked("Wallpaper damon")
    def wallpaper(self, sender):
        sender.state = not sender.state
        if sender.state:
            rumps.alert(message='You are now running wallpaper daemon', ok='OK')
            self.editor.interrupted = False
            self.editor.run()
        else:
            self.editor.interrupted = True

    @rumps.clicked("Next wallpaper")
    def next_wallpaper(self,_):
        self.editor.choose_random_image()

    @rumps.clicked("Quit")
    def clean_up_before_quit(self,_):
        print("Quit application")
        rumps.quit_application()

if __name__ == "__main__":
    Bar().run()
