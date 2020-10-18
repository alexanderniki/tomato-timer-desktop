import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GObject

from app.configuration import Configuration, config


class IntervalSelector(Gtk.Box):

    _text: str = ''
    _value: int = 0
    _min_value = 1
    _max_value = 90

    vbox = None
    hbox = None
    label = None
    slider = None
    spin_button = None
    adjustment = None

    def __init__(self, adjustment: Gtk.Adjustment):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.adjustment = adjustment
        self.create()

    def create(self):
        """
        Setup widget layout
        """
        self.hbox = Gtk.Box(Gtk.Orientation.HORIZONTAL, spacing=8)
        self.hbox_label = Gtk.Box(Gtk.Orientation.HORIZONTAL, spacing=8)
        self.label = Gtk.Label(self._text)
        self.adjustment.connect("value-changed", self.on_adjustment_changed)

        self.create_slider()
        self.create_spin_button()
        self.pack_ui()

    def create_slider(self):
        self.slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.adjustment)
        self.slider.set_value(self._value)
        self.slider.set_digits(0)  # Remove extra digits after decimal point while moving the slider.
        #self.slider.connect("value-changed", self.on_slider_changed)

    def create_spin_button(self):
        self.spin_button = Gtk.SpinButton()
        self.spin_button.set_adjustment(self.adjustment)
        self.spin_button.set_value(self._value)
        #self.spin_button.connect("value-changed", self.on_spinbutton_changed)

    def pack_ui(self):
        self.hbox.pack_start(self.slider, True, True, 0)
        self.hbox.pack_start(self.spin_button, False, True, 0)
        self.hbox_label.pack_start(self.label, False, False, 0)
        self.pack_start(self.hbox_label, False, True, 0)
        self.pack_start(self.hbox, False, True, 0)


    # Properties:

    @property
    def value(self) -> int:
        """
         Current value

         :return: current value
        """
        return self._value

    @value.setter
    def value(self, value: int):
        """
        Set value

        :param value: new value
        :type value: int

        :return: None
        """
        self._value = value
        self.adjustment.set_value(value)

    @property
    def text(self) -> str:
        """
        Widget label

        :return: current label
        """
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text
        self.label.set_text(self._text)

    # Callbacks:

    def on_slider_changed(self, event):
        self._value = int(self.adjustment.get_value())
        self.emit("changed")

    def on_spinbutton_changed(self, event):
        self._value = int(self.adjustment.get_value())
        self.emit("changed")

    def on_adjustment_changed(self, event):
        self._value = int(self.adjustment.get_value())
        self.emit("changed")

    # Signals:

    @GObject.Signal
    def changed(self):
        pass