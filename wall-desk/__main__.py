"""WallpDesk

Simple os x application for setting wallpaper and
desktop file name commands

TO DO:
    do two modes one needs to create process wallpd - daemon and second controller to controll module but via command line no gui
"""
__author__ = 'ales lerch'

import argparse
from wallpaper import Editor
from desktop import Daemon
from os.path import isfile
from database import DB_lite, HOME
from subprocess import Popen, PIPE, call

def argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            'urls', nargs='*', help='Url of thread with images, Multiple urls in one command is posssible', default =[]
            )
    parser.add_argument('-r', '--reload', action='store_true', help='Refresh script every 5 minutes to check for new images')
    parser.add_argument('-l', '--last', action='store_true', help='Show history information about downloading images')
    parser.add_argument('-s', '--selenium', action='store_true', help='Activate selenium mode to load site with healess mode (use for sites that load iamges later)')
    parser.add_argument('-i', '--ignore', action='store_true', help='Ignore title setup just use founded on site')
    return parser.parse_args()


def main(path_):
    db = DB_lite()
    #default_wall = self.db.get_wall_path()
    editor = Editor()
    desktop = Daemon()

def resest_library(editor):
    if editor:
        editor.reset_library()

def setup_directory():
    cmd = b"""choose folder with prompt "Please select an output folder:" """
    proc = Popen(["osascript", '-'], stdin=PIPE, stdout=PIPE)
    file_path, _ = proc.communicate(cmd)
    file_path = file_path.decode("utf-8").replace("alias Macintosh HD",'').replace('\n','').replace(':','/')
    if self.default_wall != file_path and proc.returncode == 0:
        print(file_path)
        self.default_wall = file_path
        self.db.set_wall_path(file_path)
        self.editor.set_loading_dir(self.default_wall)

def activate_desktop():
    cmd = b"""display notification "You are now running desktop daemon" with title\
            "WallpDesk" subtitle "Desktop Activation" """
    Popen(["osascript", '-'], stdin=PIPE, stdout=PIPE).communicate(cmd)
    print("Activating desktop manager")
    self.desktop.shut_down("P_desktop_manager")
    self.desktop.run()

def activate_wallpaper(editor, def_wallapers_path, title):
    try:
        if def_wallapers_path:
            cmd = f"""display notification "You are now running wallpaper for {sender.title} daemon" with title\
                    "WallpDesk" subtitle "Wallpaper Activation" """
            Popen(["osascript", '-'], stdin=PIPE, stdout=PIPE).communicate(cmd.encode())
            r_time = {"5 minutes": 300,"15 minutes": 900,"30 minutes": 1800, "1 hour": 3600}
            try:
                #print(sender.title,r_time[str(sender.title)])
                #print(r_time[str(sender.title)])
                editor.time = r_time[str(title)]
                editor.shut_down("P_changing_image")
                editor.run(self.editor.check_alive_process())
            except KeyError:
                pass
                #(f"{sender.title} key not an option!")
                #if not any([y.sate for y in [ for x in self.menu["Activate Wallpaper"]]):
                #list_ = []
                #for aw in self.default_times:
                #    list_.append(self.menu["Activate Wallpaper"][aw].state)
                #if not any(list_):
                #    print("killing process P_changing_image")
                #    self.editor.shut_down("P_changing_image")
        else:
            print("No input path for images set!")
    except Exception as e:
        print(e)

def next_wallpaper():
    print("Clicked next wallpaer")
    try:
        self.editor.choose_random_image(self.editor.check_alive_process())
    except Exception as e:
        print(e)

def previous_wallpaper(self,_):
    print("Clicked previous wallpaer")
    self.editor.choose_last_image()

def install():
    #os.makedirs(path_, exist_ok=True)
    pass

if __name__ == "__main__":
    main(f"{HOME}/Library/Application Support/WallpDesk")
