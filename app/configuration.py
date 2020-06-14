"""
App configuration
"""

import json
import datetime


class Configuration:

    # Constants
    CONFIG_FILE: str = 'app/config.json'
    LOC_FILE: str = 'app/strings.json'
    LOCALE = 'EN'  # Default locale - English
    DEBUG: bool = True

    # Windows of the app
    windows = {}

    # Widgets of the app
    widgets = {}

    messages = {}

    # Intervals
    tomato: int = 0
    short_break: int = 0
    long_break: int = 0

    # Statistics
    tomatoes: int = 0
    short_breaks: int = 0
    long_breaks: int = 0

    def __init__(self):
        self.get_configuration()
        self.get_messages(self.LOCALE)

    def get_tomato(self):
        return self.tomato

    # Setters

    def set_tomato(self, value: int):
        if value > 0:
            self.tomato = value
            self.update_interval('tomato', value)
        else:
            pass

    def set_short_break(self, value: int):
        if self.value > 0:
            self.short_break = value
            self.update_interval('short_break', value)
        else:
            pass

    def set_long_break(self, value: int):
        if self.value > 0:
            self.long_break = value
            self.update_interval('long_break', value)
        else:
            pass

    def get_messages(self, locale):

        with open(self.LOC_FILE, 'r', encoding="utf8") as f:
            raw_data = json.load(f)
            json_messages = raw_data['strings'][locale]
            self.messages = json_messages
            f.close()

    def get_configuration(self):

        with open(self.CONFIG_FILE, 'r', encoding="utf8") as f:
            raw_data = json.load(f)
            configuration = raw_data['configuration']

            # Q: why can't I use values straight from JSON? Why should I read them to variables first?
            self.LOCALE = configuration['locale']
            self.DEBUG = configuration['debug']
            self.tomato = configuration['intervals']['tomato']
            self.short_break = configuration['intervals']['short_break']
            self.long_break = configuration['intervals']['long_break']
            f.close()

    def to_seconds(self, minutes: int) -> int:

        """
        Construct intervals in seconds
        """
        seconds = minutes * 60
        return seconds

    def to_interval(self, seconds: int):

        """
        Construct proper text interval before displaying it in the UI
        """
        interval = datetime.timedelta(seconds=seconds)
        return interval

    def update_interval(self, interval: str, value: float) -> None:
        a_file = open(self.CONFIG_FILE, 'r+', encoding="utf8")
        json_config = json.load(a_file)
        a_file.close()

        json_config['configuration']['intervals'][interval] = value

        b_file = open(self.CONFIG_FILE, 'w', encoding="utf8")
        if self.DEBUG == True:
            print(json_config)
        b_file.write(json.dumps(json_config, indent=4, sort_keys=True, ensure_ascii=False))
        #json.dump(json_config, b_file)
        b_file.close()


config = Configuration()
