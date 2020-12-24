import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

from app.configuration import config
from app.interval_selector import IntervalSelector
from app.logger import log


class SettingsWindowBox(Gtk.Box):

    def __init__(self):

        self.WIDGET_SPACING = 8
        # self.configuration = config
        config.widgets['settings-window-box'] = self
        log.debug(config.widgets)
        self.setup_ui()

    def setup_ui(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=self.WIDGET_SPACING)
        self.modify_font(Pango.FontDescription("Sans"))

        self.set_box_margin(8)

        # New intervals:
        # Todo: make separate adjustments per interval.

        # Adjustments
        self.adjustment_tomato = Gtk.Adjustment(1, 1, 90, 1, 1, 0)
        self.adjustment_shortbreak = Gtk.Adjustment(1, 1, 30, 1, 1, 0)
        self.adjustment_longbreak = Gtk.Adjustment(1, 1, 45, 1, 1, 0)

        self.interval_tomato = IntervalSelector(self.adjustment_tomato)
        self.interval_tomato.text = config.messages['tomato']
        self.interval_tomato.value = config.tomato
        # self.interval_tomato.connect('changed', self.on_interval_event)
        self.interval_tomato.adjustment.connect("value-changed", self.on_interval_event, "tomato")

        self.interval_short_break = IntervalSelector(self.adjustment_shortbreak)
        self.interval_short_break.text = config.messages['short-break']
        self.interval_short_break.value = config.short_break
        # self.interval_short_break.connect('changed', self.on_interval_event)
        self.interval_short_break.adjustment.connect("value-changed", self.on_interval_event, "short_break")

        self.interval_long_break = IntervalSelector(self.adjustment_longbreak)
        self.interval_long_break.text = config.messages['long-break']
        self.interval_long_break.value = config.long_break
        # self.interval_long_break.connect('changed', self.on_interval_event)
        self.interval_long_break.adjustment.connect("value-changed", self.on_interval_event, "long_break")

        # END new intervals

        """self.create_tomato_setting()
        self.create_shortbreak_settings()
        self.create_longbreak_settings()"""
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
        """self.pack_start(self.hbox_tomato, False, False, 0)
        self.pack_start(self.hbox_shortbreak, False, True, 0)
        self.pack_start(self.hbox_longbreak, False, True, 0)
        self.pack_start(self.button_apply, False, True, 0)"""
        # ---
        self.pack_start(self.interval_tomato, False, True, 0)
        self.pack_start(self.interval_short_break, False, True, 0)
        self.pack_start(self.interval_long_break, False, True, 0)
        self.pack_start(self.button_apply, False, True, 0)

    def create_apply_button(self):
        self.button_apply = Gtk.Button(config.messages['settings-apply'])
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
        print("on_apply_button_clicked(self, event, *args)" + str(event))
        if config.widgets['main-window-box'].timer_active:
            print("Timer is active")
            config.update_interval('tomato', self.interval_tomato.value)
            config.update_interval('short_break', self.interval_short_break.value)
            config.update_interval('long_break', self.interval_long_break.value)
            config.get_configuration()
        else:
            print("Timer inactive")
            config.update_interval('tomato', self.interval_tomato.value)
            config.update_interval('short_break', self.interval_short_break.value)
            config.update_interval('long_break', self.interval_long_break.value)
            config.get_configuration()
            current_interval = config.widgets["main-window-box"].current_interval_type
            print("Current interval" + current_interval)
            if current_interval == 'tomato':
                config.widgets["main-window-box"].set_interval(config.tomato)
                config.widgets["main-window-box"].update_label()
            elif current_interval == 'short-break':
                config.widgets["main-window-box"].set_interval(config.short_break)
                config.widgets["main-window-box"].update_label()
            else:
                config.widgets["main-window-box"].set_interval(config.long_break)
                config.widgets["main-window-box"].update_label()

    def on_interval_event(self, event, *args):
        if args[0] == "tomato":
            print("Interval changed. Type: " + args[0] + ". Value: " + str(self.interval_tomato.value))
        elif args[0] == "short_break":
            print("Interval changed. Type: " + args[0] + ". Value: " + str(self.interval_short_break.value))
        else:
            print("Interval changed. Type: " + args[0] + ". Value: " + str(self.interval_long_break.value))
        pass
