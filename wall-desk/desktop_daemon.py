"""Desktop daemon

This is desktop deamon for checking desktop files
"""
__author__ = 'ales lerch'

import os
import re
import time
import shutil
import subprocess
from enum import Enum
from database import HOME
from wallpaper import Wallpaper
from multiprocessing import Process

class Lexer_state(Enum):
    start = 1
    word = 2
    operation = 3

class DesktopDaemon(Wallpaper):

    def __init__(self, delay = 5):
        super().__init__(f"{HOME}/Desktop/")

    def check_desktop(self):
        while True:
            time.sleep(1.5)
            super().get_file_images(True)
            for supported_file_name in filter(lambda data: data.startswith('@'), self.img_files):
                print(supported_file_name)
                self.evaluate(self.lexer(supported_file_name))

    def run(self):
        Process(target=self.check_desktop, name = "P_desktop_manager", daemon = True).start()

    def lexer(self,text):
        """ token stands for file name, commands are operations
        that should be done"""
        token = ""
        command = ""
        #commands = []
        state = Lexer_state.start
        identify = re.compile("[a-zA-Z0-9_\.-]+")
        orginal = text

        while text != "":
            if state == Lexer_state.start:
                if text[0] == ' ':
                    text = text[1:]
                elif text[0] == '@':
                    text = text[1:]
                    state = Lexer_state.operation
                elif identify.match(text[0]):
                    state = Lexer_state.word
                    token += text[0]
                    text = text[1:]
                else:
                    #print("[Error]Not valid charatect")
                    text = text[1:]

            elif state == Lexer_state.operation:
                if text[0] == '{':
                    text = text[1:]
                elif identify.match(text[0]):
                    command += text[0]
                    text = text[1:]
                elif text[0] == '}':
                    text = text[1:]
                    #commands.append(command.lower())
                    #command = ""
                    state = Lexer_state.start

            elif state == Lexer_state.word:
                if identify.match(text[0]):
                    token += text[0]
                    text = text[1:]
                else:
                    #should contiue? file_name should be done
                    state = Lexer_state.start

        return (orginal, token,[command])

    def evaluate(self, args):

        def desktop(org, file_):
            subprocess.call(["mv", "-n", f"{HOME}/Desktop/{org}",f"{HOME}/Desktop/{file_}"])
            super(Daemon,self).set_wallpaper(
                    f"{HOME}/Desktop/{file_}")

        original, file_name, commands = args
        # refcatoring needed for this ugly thing bellow
        command_list = {
                "pixiv": lambda n :
                subprocess.call(["mv","-n",f"{HOME}/Desktop/{n[0]}",
                    f"{HOME}/Pictures/pix-girls/{n[1]}"]),
                "girls": lambda n :
                subprocess.call(["mv","-n",f"{HOME}/Desktop/{n[0]}",
                    f"{HOME}/Pictures/Madchen/{n[1]}"]),
                "img": lambda n :
                subprocess.call(["mv","-n",f"{HOME}/Desktop/{n[0]}",
                    f"{HOME}/Pictures/{n[1]}"]),
                "meme": lambda n : subprocess.call(["mv",
                    "-n",f"{HOME}/Desktop/{n[0]}",
                    f"{HOME}/Pictures/Meme/{n[1]}"]),
                "daytime" : lambda n :
                subprocess.call(["mv","-n",f"{HOME}/Desktop/{n[0]}",f"{HOME}/TimeDayWal/{n[1]}"]),
                "mv" : lambda f, t :
                subprocess.call(["mv","-n",f"{HOME}/Desktop/{f}",f"{os.path.abspath(t)}"]),
                "trash" : lambda n :
                subprocess.call(["mv",f"{HOME}/Desktop/{n[0]}",f"{HOME}/.Trash/{n[1]}"]),
                "wall" : lambda n : desktop(n[0], n[1]),
                }

        # control inputs
        try:
            if len(commands) > 1:
                # more commands
                if len(commands) == 2:
                    command_list[commands[0]](file_name,commands[1])
                else:
                    # so far there are no special tasks for more commands
                    command_list[commands[0]](file_name,commands)
            else:
                # print("calling command",commands)
                command_list[commands[0]]((original,file_name))
        except KeyError:
            pass

