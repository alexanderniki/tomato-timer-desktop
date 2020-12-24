import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

from app.main_window_gtk import MainWindow
from app.configuration import Configuration, config


# configuration = Configuration()

window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
