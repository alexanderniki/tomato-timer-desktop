import time
import datetime
import logging

import locale
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

from app.main_window_box import MainWindowBox
from app.configuration import Configuration, config


class MainWindow(Gtk.Window):

    def __init__(self):

        logger = logging.getLogger()
        logging.basicConfig(level="DEBUG")
        logger.info("Starting the app")

        config.windows['main_window'] = self

        Gtk.Window.__init__(self, title=config.messages['app-title'])
        self.mwb = MainWindowBox()
        self.add(self.mwb)
        self.get_system_info()

        self.connect('destroy', Gtk.main_quit)

    def get_system_info(self):
        self.system_language = locale.getdefaultlocale()
        print(self.system_language)


if __name__ == "__main__":

    configuration = Configuration()

    window = MainWindow()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()