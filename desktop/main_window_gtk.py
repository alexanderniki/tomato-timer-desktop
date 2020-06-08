import time
import datetime

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

from main_window_box import MainWindowBox
from configuration import Configuration


class MainWindow(Gtk.Window):

    def __init__(self, config: Configuration):

        self.configuration = config
        self.configuration.windows['main_window'] = self

        Gtk.Window.__init__(self, title=self.configuration.messages['app_title'])
        #self.set_default_size(320, 240)
        self.mwb = MainWindowBox(self.configuration)
        #self.set_titlebar(self.mwb.header_bar)
        self.add(self.mwb)

        self.connect('destroy', Gtk.main_quit)


if __name__ == "__main__":

    configuration = Configuration()

    window = MainWindow(configuration)
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()