"""Desktop daemon

This is desktop deamon for checking desktop files
"""
__author__ = 'ales lerch'

import re
from enum import Enum

class Lexer_state(Enum):
    s = 1
    operation = 2
    word = 3

class Desk_deamon:

    def __init__(self):
        self.files = []
        self.types = (".jpg",".png",".jpeg",".tiff")
        self.tokens = []
        self.commands = []

    def get_dfiles(self):
        for f in os.listdir("~/Desktop/"):
            if f.splitext[1] in self.types:
                self.files.append(f)

    def lexer(self,text):
        identify = re.compitle("\w*\_*\(?\)?\.*-*")
        state = Lexer_state.s
        token = ""
        command = ""
        while text != "":
            if state == Lexer_state.s:
                if text[0] in [' ']:
                    text = text[1:]
                elif text[0] in ['@','{']:
                    text = text[1:]
                    state = Lexer_state.operation
                elif identify.match(text[0]):
                    state = Lexer_state.word
                    token += text[0]
                    text = text[1:]
                else:
                    print("[Error]Not valid charatect")

            elif state == Lexer_state.operation:
                if text[0] in ['@','{']:
                    text = text[1:]
                elif identify.match(text[0]):
                    command += text[0]
                    text = text[1:]
                elif text[0] == '}':
                    text = text[1:]
                    #saving command more commands
                    self.commands.append(command)
                    command = ""
                    state = Lexer_state.s
            elif state == Lexer_state.word:
                if identify.match(text[0]):
                    token += text[0]
                    text = text[1:]
                else:
                    state = Lexer_state.s
                    #saving token should be just one
                    self.tokens.append(token)
                    token =""

    def evaluate(self):
        pass

