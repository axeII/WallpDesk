"""Menu_bar

Menu bar module for setting menu bar setup for OSX
"""
__author__ = 'ales lerch'

import rumps
import desktop
import wallpaper

class Bar(rumps.App):

    def __init__(self):
        super(Bar, self).__init__("Some faking Awesome App")
        self.menu = ["Desktop daemon On/Off", "Wallpaper damon On/Off", None
                ,"Next wallpaper", "Quit"]
        self.quit_button = None
        self.icon = "test.png"
        self.template = True
        self.title = None

        self.editor = wallpaper.Editor("./testimg").run()
        self.desktop = desktop.Daemon().run()

    @rumps.clicked("Desktop daemon On/Off")
    def on_off_test(self, sender):
        #rumps.notification(title='Hi', subtitle='There.', message='Friend!', sound=does_something.sound, data=my_data)
        sender.state = not sender.state
        if sender.state:
            self.desktop.run_ = True
            rumps.alert(message='You are now running desktop daemon', ok='OK')
        else:
            self.desktop.run_ = False

    @rumps.clicked("Wallpaper damon On/Off")
    def wallpaper(self, sender):
        sender.state = not sender.state
        if sender.state:
            rumps.alert(message='You are now running wallpaper daemon', ok='OK')
            self.editor.run_ = True
        else:
            self.editor.run_ = False


    @rumps.clicked("Next wallpaper")
    def next_wallpaper(self,_):
        print("setting next wallpar yeah")

    @rumps.clicked("Quit")
    def clean_up_before_quit(self,_):
        print('execute clean up code')
        rumps.quit_application()

if __name__ == "__main__":
    Bar().run()
    pass
