import configparser
import os


class AppSettings:
    
    #  Tomato settings:
    Tomato = 25
    SBreak = 5
    LBreak = 15
    
    #  Statistic settings:
    Tomatoes = 0
    SBreaks = 0
    LBreaks = 0
    
    #  Application:
    MainWindow = None
    TrayIcon = None
    AboutWindow = None
    PlannerWindow = None
    PlannerWidget = None
    SettingsWindow = None
    StatisticWindow = None
    SysTrayMenu = None
    MainMenu = None
    SettingsWindow = None
    SettingsWidget = None
    IntervalSettingSlider = None
    
    #  Window list (dictionary)
    window_list = {}
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = current_dir + "/grapetomato.conf"

    # Debugging flag
    DEBUG = 1

    def __init__(self):
        self.initialize()
        
    def initialize(self):
        """
        Read settings from a file like grapetomato.conf
        """
        self.read_settings()

    def getTomato(self):
        return self.Tomato

    def getSBrake(self):
        return self.SBreak

    def getLBreak(self):
        return self.LBreak

    def setTomato(self, tomato):
        self.Tomato = tomato
    
    def setSBreak(self, sbreak):
        self.SBreak = sbreak
        
    def setLBreak(self, lbreak):
        self.LBreak = lbreak
        
    def update_settings(self):
        # generate new config file
        config_parser = configparser.ConfigParser()
        config_file = open(self.config_file, 'w')
        config_parser.add_section('Intervals')
        config_parser.set('Intervals', 'tomato', str(self.Tomato))
        config_parser.set('Intervals', 'large_break', str(self.LBreak))
        config_parser.set('Intervals', 'small_break', str(self.SBreak))
        config_parser.write(config_file)
        
    def read_settings(self):
        #  read intervals
        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_file)
        intervals_section = config_parser['Intervals']
        self.Tomato = int(intervals_section['tomato'])
        self.SBreak = int(intervals_section['small_break'])
        self.LBreak = int(intervals_section['large_break'])
