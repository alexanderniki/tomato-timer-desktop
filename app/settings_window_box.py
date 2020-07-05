import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

from app.configuration import Configuration, config


class SettingsWindowBox(Gtk.Box):

    def __init__(self, config: Configuration):

        self.WIDGET_SPACING = 8
        # self.configuration = config
        config.widgets['settings-window-box'] = self
        print(config.widgets)
        self.setup_ui()

    def setup_ui(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=self.WIDGET_SPACING)
        self.modify_font(Pango.FontDescription("Sans"))

        self.set_box_margin(8)

        self.create_tomato_setting()
        self.create_shortbreak_settings()
        self.create_longbreak_settings()
        self.create_apply_button()
        self.create_layouts()

    # Setters:

    def set_box_margin(self, value: int) -> None:
        self.set_margin_top(value)
        self.set_margin_left(value)
        self.set_margin_right(value)
        self.set_margin_bottom(value)

    # Methods:

    def create_layouts(self):
        self.pack_start(self.hbox_tomato, False, False, 0)
        self.pack_start(self.hbox_shortbreak, False, True, 0)
        self.pack_start(self.hbox_longbreak, False, True, 0)
        self.pack_start(self.button_apply, False, True, 0)

    def create_tomato_setting(self):
        self.label_tomato = Gtk.Label(config.messages['tomato'])
        self.vbox_tomato = Gtk.Box(spacing=self.WIDGET_SPACING)
        self.hbox_tomato = Gtk.Box(spacing=self.WIDGET_SPACING)
        self.adjustment_tomato = Gtk.Adjustment(1, 1, 90, 1, 1, 0)

        self.slider_tomato = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.adjustment_tomato)
        self.slider_tomato.set_value(config.tomato)
        self.slider_tomato.set_digits(0)  # Remove extra digits after decimal point while moving the slider.
        self.slider_tomato.connect("value-changed", self.on_tomato_slider_changed)


        self.spinbutton_tomato = Gtk.SpinButton()
        self.spinbutton_tomato.set_adjustment(self.adjustment_tomato)
        self.spinbutton_tomato.set_value(config.tomato)
        self.spinbutton_tomato.connect("value-changed", self.on_tomato_spinbutton_changed)

        self.hbox_tomato.pack_start(self.label_tomato, True, True, 0)
        self.hbox_tomato.pack_start(self.slider_tomato, True, True, 0)
        self.hbox_tomato.pack_start(self.spinbutton_tomato, False, True, 0)

    def create_shortbreak_settings(self):
        self.label_shortbreak = Gtk.Label(config.messages['short-break'])
        self.hbox_shortbreak = Gtk.Box(spacing=self.WIDGET_SPACING)
        self.adjustment_shortbreak = Gtk.Adjustment(1, 1, 30, 1, 1, 0)

        self.slider_shortbreak = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.adjustment_shortbreak)
        self.slider_shortbreak.set_value(config.short_break)
        self.slider_shortbreak.set_digits(0)  # Remove extra digits after decimal point while moving the slider.
        self.slider_shortbreak.connect("value-changed", self.on_shortbreak_slider_changed)

        self.spinbutton_shortbreak = Gtk.SpinButton()
        self.spinbutton_shortbreak.set_adjustment(self.adjustment_shortbreak)
        self.spinbutton_shortbreak.set_value(config.short_break)
        self.spinbutton_shortbreak.connect("value-changed", self.on_shortbreak_spinbutton_changed)

        self.hbox_shortbreak.pack_start(self.label_shortbreak, True, True, 0)
        self.hbox_shortbreak.pack_start(self.slider_shortbreak, True, True, 0)
        self.hbox_shortbreak.pack_start(self.spinbutton_shortbreak, False, True, 0)

    def create_longbreak_settings(self):
        self.label_longbreak = Gtk.Label(config.messages['long-break'])
        self.hbox_longbreak = Gtk.Box(spacing=self.WIDGET_SPACING)
        self.adjustment_longbreak = Gtk.Adjustment(1, 1, 45, 1, 1, 0)

        self.slider_longbreak = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.adjustment_longbreak)
        self.slider_longbreak.set_value(config.short_break)
        self.slider_longbreak.set_digits(0)  # Remove extra digits after decimal point while moving the slider.
        self.slider_longbreak.connect("value-changed", self.on_longbreak_slider_changed)

        self.spinbutton_longbreak = Gtk.SpinButton()
        self.spinbutton_longbreak.set_adjustment(self.adjustment_longbreak)
        self.spinbutton_longbreak.set_value(config.long_break)
        self.spinbutton_longbreak.connect("value-changed", self.on_longbreak_spinbutton_changed)

        self.hbox_longbreak.pack_start(self.label_longbreak, True, True, 0)
        self.hbox_longbreak.pack_start(self.slider_longbreak, True, True, 0)
        self.hbox_longbreak.pack_start(self.spinbutton_longbreak, False, True, 0)

    def create_apply_button(self):
        self.button_apply = Gtk.Button("Apply")
        self.button_apply.connect("clicked", self.on_apply_button_clicked)

    def update_configuration(self):
        pass

    # Callbacks:

    def on_tomato_slider_changed(self, event, *args):
        # Save changes to JSON config:
        #self.configuration.update_interval('tomato', self.slider_tomato.get_value())
        config.get_configuration()
        # Update UI:
        #self.configuration.widgets['main-window-box'].set_interval(self.slider_tomato.get_value())
        #self.configuration.widgets['main-window-box'].update_label()

    def on_tomato_spinbutton_changed(self, event, *args):
        # self.adjustment_tomato.set_value(self.slider_tomato.get_value())
        # self.configuration.update_interval('tomato', self.slider_tomato.get_value())
        pass

    def on_shortbreak_slider_changed(self, event, *args):
        #self.configuration.update_interval('short_break', self.slider_shortbreak.get_value())
        config.get_configuration()
        #self.configuration.widgets['main-window-box'].set_interval(self.slider_shortbreak.get_value())
        #self.configuration.widgets['main-window-box'].update_label()

    def on_shortbreak_spinbutton_changed(self, event, *args):
        # self.configuration.update_interval('short_break', self.slider_shortbreak.get_value())
        pass

    def on_longbreak_slider_changed(self, event, *args):
        # self.configuration.update_interval('long_break', self.slider_longbreak.get_value())
        pass

    def on_longbreak_spinbutton_changed(self, event, *args):
        #self.configuration.update_interval('long_break', self.slider_longbreak.get_value())
        pass

    def on_slider_changed(self, event, *args):
        self.tom_spin.set_value(self.tom_slider.get_value())

    def on_spinbutton_changed(self, event, *args):
        self.slider_adj.set_value(self.tom_spin.get_value())

    def on_apply_button_clicked(self, event, *args):
        print("on_apply_button_clicked(self, event, *args)")
        if config.widgets['main-window-box'].timer_active:
            print("Timer is active")
            config.update_interval('tomato', self.slider_tomato.get_value())
            config.update_interval('short_break', self.slider_shortbreak.get_value())
            config.update_interval('long_break', self.slider_longbreak.get_value())
            config.get_configuration()
        else:
            print("Timer inactive")
            config.update_interval('tomato', self.slider_tomato.get_value())
            config.update_interval('short_break', self.slider_shortbreak.get_value())
            config.update_interval('long_break', self.slider_longbreak.get_value())
            config.get_configuration()
            if config.widgets['main-window-box'].current_interval_type == 'tomato':
                config.set_tomato(self.slider_tomato.get_value())
                config.widgets['main-window-box'].current_interval = self.slider_tomato.get_value()
                config.widgets['main-window-box'].time_remaining = self.slider_tomato.get_value()*60
                config.widgets['main-window-box'].update_label()
            elif config.widgets['main-window-box'].current_interval_type == 'short-break':
                config.widgets['main-window-box'].current_interval = self.slider_shortbreak.get_value()
                config.widgets['main-window-box'].time_remaining = self.slider_shortbreak.get_value()*60
                config.widgets['main-window-box'].update_label()
            else:
                config.widgets['main-window-box'].current_interval = self.slider_longbreak.get_value()
                config.widgets['main-window-box'].time_remaining = self.slider_longbreak.get_value() * 60
                config.widgets['main-window-box'].update_label()
        config.get_configuration()
