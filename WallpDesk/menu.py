"""Menu_bar

Menu bar module for setting menu bar setup for OSX
"""
__author__ = 'ales lerch'

import rumps
import desktop
import wallpaper
from wall import HOME
from os.path import isfile
from database import DB_lite
from subprocess import Popen, PIPE

class Bar(rumps.App):

    def __init__(self):
        super().__init__("WallpDesk")
        self.menu = ["About",None,"Setup Directory",
                "Reset Database", None, "Activate Desktop",
                {"Activate Wallpaper":
                [rumps.MenuItem("5 minutes", callback=self.activate),
                 rumps.MenuItem("15 minutes", callback=self.activate),
                 rumps.MenuItem("30 minutes", callback=self.activate),
                 rumps.MenuItem("1 hour", callback=self.activate),
                ]
                }, None, "Next Wallpaper", "Previous Wallpaper", None, "Quit"]
        self.default_times = ("5 minutes","15 minutes","30 minutes", "1 hour")
        self.db = DB_lite()
        self.default_wall = self.db.get_wall_path()
        self.quit_button = None
        self.template = True
        self.title = None
        if isfile("images/menu_bar.png"):
            self.icon = "images/menu_bar.png"
        else:
            self.title = "Icon not found"

        self.editor = wallpaper.Editor()
        self.desktop = desktop.Daemon()

    @rumps.clicked("About")
    def about(self, _):
        rumps.Window(message="\t   WallpDesk (0.1.0)", title="\tAbout WallpDesk",
                default_text="""\tVersion: 0.1.0\n\tLicence: MIT\n\tAuthor: Ales Lerch
\nHow to use:\n 1) Setup directory
2) Wait for image to load to database with
image control (Notification will notify you.
3) Start damon and choose time interval
Desktop daemon is used for managing files at desktop.
Use: @{command}file (readme.md)""", dimensions=(210, 250)).run()

    @rumps.clicked("Reset Database")
    def reset_db(self, _):
        self.editor.reset_library()

    @rumps.clicked("Setup Directory")
    def settings(self, _):
        cmd = b"""choose folder with prompt "Please select an output folder:" """
        proc = Popen(["osascript", '-'], stdin=PIPE, stdout=PIPE)
        file_path, _ = proc.communicate(cmd)
        file_path = file_path.decode("utf-8").replace("alias Macintosh HD",'').replace('\n','').replace(':','/')
        if self.default_wall != file_path and proc.returncode == 0:
            print(file_path)
            self.default_wall = file_path
            self.db.set_wall_path(file_path)
            self.editor.set_loading_dir(self.default_wall)

    @rumps.clicked("Activate Desktop")
    def on_off_test(self, sender):
        """ notifications are so far broken in rumps
        rumps.notification(title='Hi', subtitle='There.', message='Friend!',
        sound=does_something.sound, data=my_data)"""
        sender.state = not sender.state
        if sender.state:
            #rumps.alert(message='You are now running desktop daemon')
            cmd = b"""display notification "You are now running desktop daemon" with title\
            "WallpDesk" subtitle "Desktop Activation" """
            Popen(["osascript", '-'], stdin=PIPE, stdout=PIPE).communicate(cmd)
            print("Activating desktop manager")
            self.desktop.shut_down("P_desktop_manager")
            self.desktop.run()
        else:
            self.desktop.shut_down("P_desktop_manager")

    def activate(self, sender):
        try:
            if self.default_wall and str(sender.title) in self.default_times:
                sender.state = not sender.state
                for ru_state in [st for st in self.default_times if st != sender.title]:
                    self.menu["Activate Wallpaper"][ru_state].state = False
                if sender.state:
                    #rumps.alert(message='You are now running wallpaper daemon', ok='OK')
                    cmd = f"""display notification "You are now running wallpaper for {sender.title} daemon" with title\
                    "WallpDesk" subtitle "Wallpaper Activation" """
                    Popen(["osascript", '-'], stdin=PIPE, stdout=PIPE).communicate(cmd.encode())
                    r_time = {"5 minutes": 300,"15 minutes": 900,"30 minutes": 1800, "1 hour":
                            3600}
                    try:
                        print(sender.title,r_time[str(sender.title)])
                        self.editor.time = r_time[str(sender.title)]
                        self.editor.shut_down("P_changing_image")
                        self.editor.run()
                    except KeyError:
                        rumps.alert(f"{sender.title} key not an option!")
                #if not any([y.sate for y in [ for x in self.menu["Activate Wallpaper"]]):
                list_ = []
                for aw in self.default_times:
                    list_.append(self.menu["Activate Wallpaper"][aw])
                    print(list_[-1])
                if not any(list_):
                    print('killing time')
                    self.editor.shut_down("P_changing_image")
            else:
                rumps.alert("No input path for images set!")
        except Exception as e:
            print(e)

    @rumps.clicked("Next Wallpaper")
    def next_wallpaper(self,_):
        print("Clicked next wallpaer")
        self.editor.choose_random_image()

    @rumps.clicked("Previous Wallpaper")
    def previous_wallpaper(self,_):
        print("Clicked previous wallpaer")
        self.editor.choose_last_image()

    @rumps.clicked("Quit")
    def clean_up_before_quit(self,_):
        import multiprocessing
        for pr in multiprocessing.active_children():
            pr.terminate()
            pr.join()
        print("Quit application")
        rumps.quit_application()

