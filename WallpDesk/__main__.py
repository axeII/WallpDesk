"""WallpDesk

Simple os x application for setting wallpaper and
desktop file name commands
"""
__author__ = 'ales lerch'

from menu import Bar
from wall import HOME
from subprocess import call

def main():
    path_ = f"{HOME}/Library/Application Support/WallpDesk"
    call(["mkdir", "-p", path_])
    walpdesk = Bar()
    walpdesk.run()

if __name__ == "__main__":
    main()
