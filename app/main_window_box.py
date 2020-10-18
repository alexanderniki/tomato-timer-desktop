import datetime
from notifypy import notify

# import gi
# gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, Pango

from app.configuration import config
from app.settings_window_box import SettingsWindowBox


class MainWindowBox(Gtk.Box):

    def __init__(self):

        config.widgets['main-window-box'] = self

        self.current_interval: int = config.tomato
        self.time_remaining: int = self.current_interval * 60  # TODO: make it with a method - don't hardcode a value*60
        self.current_interval_type: str = 'tomato'
        self.timer_active: bool = False
        self._setup_ui()

    def _setup_ui(self):

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.modify_font(Pango.FontDescription("Sans"))
        self.set_box_margin(8)

        self.frame = Gtk.Frame()

        self.label_time_remaining = Gtk.Label(self._interval(self.time_remaining))
        self.label_time_remaining.modify_font(Pango.FontDescription("Sans Light 48"))
        #self.pack_start(self.label_time_remaining, True, True, 0)

        self.frame.add(self.label_time_remaining)
        self.pack_start(self.frame, True, True, 0)

        self.hbox_buttons = Gtk.Box(spacing=8)
        self.btn_startstop = Gtk.Button(config.messages['btn-start'])
        self.btn_startstop.connect("clicked", self.on_button_pressed)
        self.btn_settings = Gtk.Button(config.messages['btn-settings'])
        self.btn_settings.connect("clicked", self.on_settings_pressed)
        self.hbox_buttons.pack_start(self.btn_startstop, True, True, 0)
        self.hbox_buttons.pack_start(self.btn_settings, True, True, 0)
        self.pack_start(self.hbox_buttons, True, True, 0)

        self.radio_tomato = Gtk.RadioButton(config.messages['tomato'])
        self.radio_tomato.connect("clicked", self.on_radio_changed, config.tomato, 'tomato')
        self.pack_start(self.radio_tomato, True, True, 0)

        self.radio_sbreak = Gtk.RadioButton.new_from_widget(self.radio_tomato)
        self.radio_sbreak.set_label(config.messages['short-break'])
        self.radio_sbreak.connect("clicked", self.on_radio_changed, config.short_break, 'short-break')
        self.pack_start(self.radio_sbreak, True, True, 0)

        self.radio_lbreak = Gtk.RadioButton.new_from_widget(self.radio_tomato)
        self.radio_lbreak.set_label(config.messages['long-break'])
        self.radio_lbreak.connect("clicked", self.on_radio_changed, config.long_break, 'long-break')
        self.pack_start(self.radio_lbreak, True, True, 0)

        #self.statusbar = Gtk.Statusbar()
        #self.statusbar.push(1, "Status: OK")
        #self.pack_start(self.statusbar, True, True, 0)

    def _interval(self, value: int) -> datetime.timedelta:
        if value >= 0:
            return datetime.timedelta(seconds=value)
        else:
            return datetime.timedelta(seconds=0)

    def _update_interval(self, event, *args):  # DEPRECATED
        self.current_interval = args[0]
        self.time_remaining = self.current_interval * 60
        self.update_label()

    # Setters:

    def set_box_margin(self, value: int) -> None:
        self.set_margin_top(value)
        self.set_margin_left(value)
        self.set_margin_right(value)
        self.set_margin_bottom(value)

    def set_interval(self, value):
        if not self.timer_active:
            if value >= 0:
                self.current_interval = value
                self.time_remaining = self.current_interval * 60
            else:
                self.current_interval = 0
                self.time_remaining = 0
        else:
            pass

    def set_status(self, new_status):
        # Work with status bar here
        pass

    # Actions:

    def update_label(self):
        self.label_time_remaining.set_text(str(self._interval(self.time_remaining)))

    def block_ui(self):
        """
        Block UI controls while the timer is active.
        Blocks interval switcher until the timer stopped
        """
        self.radio_tomato.set_sensitive(False)
        self.radio_sbreak.set_sensitive(False)
        self.radio_lbreak.set_sensitive(False)

    def release_ui(self):
        """
        Unblock UI controls when timer in not active
        """
        self.radio_tomato.set_sensitive(True)
        self.radio_sbreak.set_sensitive(True)
        self.radio_lbreak.set_sensitive(True)

    def update_time(self):
        """
        Timer's callback
        """
        if self.time_remaining == 0:
            self.stop_timer()
            self.timer_active = False
            # Update interval and label after stopping the timer
            self.set_interval(self.current_interval)
            self.update_label()
            #self.show_notification_dialog()
            return False
        else:
            self.timer_active = True
            self.time_remaining -= 1
            self.label_time_remaining.set_text(str(self._interval(self.time_remaining)))
        return True

    def start_timer(self):
        self.timer_active = True
        self.btn_startstop.set_label(config.messages['btn-stop'])
        self.block_ui()
        self.timer = GObject.timeout_add(1000, self.update_time)

    def stop_timer(self):
        self.timer_active = False
        self.send_notification()
        self.btn_startstop.set_label(config.messages['btn-start'])
        GObject.source_remove(self.timer)
        self.set_interval(self.current_interval)
        self.update_label()
        self.release_ui()

    def show_notification_dialog(self):
        # Don't use it!
        dialog = Gtk.Dialog()
        dialog.set_title("A Gtk+ Dialog")
        dialog.set_modal(True)
        dialog.show_all()

    def send_notification(self):
        notification = notify()
        notification.title = "Grape tomato"
        notification.message = "Time's up!"
        notification.icon = ""
        notification.send()

    # Callbacks

    def on_radio_changed(self, event, *args):
        """
        Switch between radio buttons
        """
        print(config.tomato)
        print(args)
        print(event)
        interval = args[0]
        interval_type = args[1]
        # What the fuck is going on here? Why print twice?
        #print(interval, interval_type)
        self.set_interval(interval)
        self.current_interval_type = interval_type
        self.update_label()
        #print(self.current_interval_type)
        if args[1] == 'tomato':
            self.set_interval(config.tomato)
            self.current_interval_type = interval_type
            self.update_label()
        elif args[1] == 'short-break':
            self.set_interval(config.short_break)
            self.current_interval_type = interval_type
            self.update_label()
        else:
            self.set_interval(config.long_break)
            self.current_interval_type = interval_type
            self.update_label()



    def on_button_pressed(self, event, *args):
        """
        Start and stop timer
        """
        if not self.timer_active:
            self.start_timer()
        else:
            self.stop_timer()

    def on_settings_pressed(self, event, *args):
        swb = SettingsWindowBox(config)
        # TODO: make it with separate Gtk.Window class
        settings_window = Gtk.Window()
        settings_window.set_default_size(360, 240)
        settings_window.set_title(config.messages['btn-settings'])
        settings_window.set_modal(True)
        settings_window.add(swb)
        settings_window.show_all()
