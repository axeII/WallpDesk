"""Wallpaper changer

This is wallpaper changer, module for changing desktop background by rules
"""
__author__ = 'ales lerch'


class Wall_changer:

    def __init__(self,dir_to_imgs = None):
        """connect this module to database one"""
        self.directory = dir_to_imgs

    def set_wallpaper(self,img):
        db_file = "~/Library/Application Support/Dock/desktoppicture.db"
        subprocess.call(["sqlite3", db_file, f"update data set value = '{img}'"])
        subprocess.call(["killall", "Dock"])

    def set_timer(self):
        """ Based on time wallpaper can change"""
        pass

    def choose_image(self):
        """choose dark or light based on time"""
        pass

    def choose_random_image(self):
        """choose dark or light based on time but random"""
        pass

    def set_directory(self):
        """set directory for choosing images to set as wallaper desktop"""
        pass


