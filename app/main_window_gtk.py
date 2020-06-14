import time
import datetime

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

from main_window_box import MainWindowBox
from configuration import Configuration, config


class MainWindow(Gtk.Window):

    def __init__(self):

        config.windows['main_window'] = self

        Gtk.Window.__init__(self, title=config.messages['app-title'])
        self.mwb = MainWindowBox()
        self.add(self.mwb)

        self.connect('destroy', Gtk.main_quit)


if __name__ == "__main__":

    configuration = Configuration()

    window = MainWindow()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()