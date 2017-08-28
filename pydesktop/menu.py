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
        self.menu = ["Desktop daemon On/Off", "Wallpaper", None
                ,"Next wallpaper", "Quit"]
        self.quit_button = None
        self.icon = "test.png"
        self.template = True
        self.title = None

        self.editor = wallpaper.Editor("./testimg")
        self.desktop = desktop.Daemon()

    @rumps.clicked("Desktop daemon On/Off")
    def on_off_test(self,_):
        rumps.notification(title='Hi', subtitle='There.', message='Friend!', sound=does_something.sound, data=my_data)
        print_button = self.menu["Desktop daemon On/Off"]
        if print_button.callback is None:
            print_button.set_callback(print_something)
        else:
            print_button.set_callback(None)

    @rumps.clicked("Wallpaper")
    def wallpaper(self,_):
        rumps.alert(message='something', ok='YES!', cancel='NO!')

    @rumps.clicked("Next wallpaper")
    def next_wallpaper(self,_):
        print("setting next wallpar yeah")

    @rumps.clicked("Quit")
    def clean_up_before_quit(self,_):
        print('execute clean up code')
        rumps.quit_application()

if __name__ == "__main__":
    #Bar().run()
    pass
