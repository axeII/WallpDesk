"""Desktop daemon

This is desktop deamon for checking desktop files
"""
__author__ = 'ales lerch'

import os
import re
import yaml
import time
import shutil
import subprocess
from enum import Enum
from database import HOME
from wallpaper import Wallpaper
from multiprocessing import Process

class LexerState(Enum):
    Q_start = 1
    Q_word = 2
    Q_operation = 3

class Token:
    def __init__(self, original_name, token_file_name = "", token_command = None):
        self.origin_name = original_name
        self.file_name = token_file_name
        self.command = token_command

    def __repr__(self):
        return f"Token::<original name: {self.origin_name}, file name: {self.file_name}, command: {self.command}>"

class DesktopDaemon(Wallpaper):

    def __init__(self, delay = 5):
        super().__init__(f"{HOME}/Desktop/")
        self.path_to_conf = f"{HOME}/.walld/config.yaml"

    def check_desktop(self):
        while True:
            time.sleep(1.5)
            super().get_all_files()
            for supported_file_name in filter(lambda data: data.startswith('@'), self.all_files):
                self.evaluate(self.lexer(supported_file_name))

    def run(self):
        Process(target=self.check_desktop, name = "P_desktop_manager", daemon = True).start()

    def lexer(self, text, f_name="", command=""):
        """
        f_name stands for file name,
        commands are operations
        """
        original = text
        identify = re.compile("[a-zA-Z0-9_\.-]+")
        state = LexerState.Q_start

        while text != "":
            if state == LexerState.Q_start:
                if text[0] == ' ':
                    text = text[1:]
                elif text[0] == '@':
                    text = text[1:]
                    state = LexerState.Q_operation
                elif identify.match(text[0]):
                    state = LexerState.Q_word
                    f_name += text[0]
                    text = text[1:]
                else:
                    print("[Error] Not valid charatect")
                    # text = text[1:]
                    return None

            elif state == LexerState.Q_operation:
                if text[0] == '{':
                    text = text[1:]
                elif identify.match(text[0]):
                    command += text[0]
                    text = text[1:]
                elif text[0] == '}':
                    text = text[1:]
                    state = LexerState.Q_start
                else:
                    return None

            elif state == LexerState.Q_word:
                if identify.match(text[0]):
                    f_name += text[0]
                    text = text[1:]
                else:
                    state = LexerState.Q_start
            """if text != "":
                if state == LexerState.Q_word:
                    return Token(original, f_name, command)
                elif state == LexerState.Q_operation:
                    return Token(original, f_name, command)
                else:
                    return None"""
        return Token(original, f_name, command)

    def evaluate(self, token, parsed_data=""):
        assert token
        with open(self.path_to_conf,'r') as conf:
            try:
                parsed_data = yaml.load(conf)
            except yaml.YAMLError as exc:
                print(exc)
        if token.command in list(parsed_data["paths"].keys()):
            subprocess.call(["mv","-n",f"{HOME}/Desktop/{token.origin_name}",os.path.join(parsed_data["paths"][token.command],f"{token.file_name}")])
        elif os.path.isdir(token.command):
            subprocess.call(["mv","-n",f"{HOME}/Desktop/{token.origin_name}",f"{token.command}/{token.file_name}"])
        else:
            print("[ERROR] Could not execute any action")
