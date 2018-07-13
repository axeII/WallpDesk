"""__main__.py

Simple os x application for setting wallpaper and
desktop file name commands

TO DO:
    do two modes one needs to create process wallpd - daemon and second controller to controll module but via command line no gui
"""
__author__ = "ales lerch"

import os
import getch
import argparse
from os.path import isfile
from database import DB_lite, HOME
from desktop_daemon import DesktopDaemon
from subprocess import call, PIPE, Popen
from wallpaper_daemon import WallpaperDaemon


def argparse_():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "urls",
        nargs="*",
        help="Url of thread with images, Multiple urls in one command is posssible",
        default=[],
    )
    parser.add_argument(
        "-r", "--reload", action="store_true", help="Realod configure file"
    )
    parser.add_argument(
        "-i",
        "--ignore",
        action="store_true",
        help="Ignore title setup just use founded on site",
    )
    return parser.parse_args()


def init_stuff():
    arguments = argparse_()
    inst_database = DB_lite()
    def_wall_path = inst_database.get_wall_path()
    inst_editor = WallpaperDaemon()
    inst_walpaper = DesktopDaemon()
    return (inst_walpaper, inst_database, inst_editor, def_wall_path)


def main(path_to_directory):
    """
    editor: for chaning wallpaper, needs direcotry from taking images
    db: application databse
    dameon: desktop dameon for supporting desktop function eg: @trash_test.file
    """
    assert path_to_directory
    install(path_to_directory)
    # init stuff
    i_wallpaper, i_db, i_editor, default_wall = init_stuff()
    if not default_wall:
        default_wall = setup_directory(None, i_db, i_editor)
    activate_desktop(i_wallpaper)
    activate_wallpaper(i_editor, default_wall)
    try:
        while getch.getch() != "q":
            pass
    except KeyboardInterrupt:
        quit()


def reset_library(editor):
    if editor:
        editor.reset_library()


def setup_directory(default_wall, db, editor):
    cmd = b"""choose folder with prompt "Please select an output folder:" """
    Popen(["osascript", "-"], stdin=PIPE, stdout=PIPE).communicate(cmd)
    file_path, _ = proc.communicate(cmd)
    file_path = (
        file_path.decode("utf-8")
        .replace("alias Macintosh HD", "")
        .replace("\n", "")
        .replace(":", "/")
    )
    if default_wall != file_path and proc.returncode == 0:
        print(file_path)
        default_wall = file_path
        db.set_wall_path(file_path)
        editor.set_loading_dir(default_wall)
        return default_wall
    return None


def activate_desktop(desktop):
    cmd = b"""display notification "You are now running desktop daemon" with title\
            "WallpDesk" subtitle "Desktop Activation" """
    Popen(["osascript", "-"], stdin=PIPE, stdout=PIPE).communicate(cmd)
    print("[INFO] Activating desktop manager")
    # desktop.shut_down("P_desktop_manager")
    desktop.run()


def activate_wallpaper(editor, def_wallapers_path):
    try:
        if def_wallapers_path:
            cmd = b"""display notification "You are now running wallpaper for daemon" with title "walld" subtitle "Wallpaper Activation" """
            Popen(["osascript", "-"], stdin=PIPE, stdout=PIPE).communicate(cmd)
            # editor.time = r_time[str(title)]
            # editor.shut_down("P_changing_image")
            editor.run()
        else:
            print("[ERROR] Path with images had not been set!")
    except Exception as err:
        print(err)


"""def next_wallpaper():
    # depreciated
    try:
        self.editor.choose_random_image(self.editor.check_alive_process())
    except Exception as e:
        print(e)

def previous_wallpaper(self,_):
    # depreciated
    self.editor.choose_last_image()
"""


def install(path):
    os.makedirs(path, exist_ok=True)


if __name__ == "__main__":
    # main(f"{HOME}/Library/Application Support/WallpDesk")
    main(f"{HOME}/.walld")
