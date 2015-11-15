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
    SettingsWindow = None
    StatisticWindow = None
    SysTrayMenu = None
    MainMenu = None
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = current_dir + "./grapetomato.conf"

    # Debugging flag
    DEBUG = 1

    def __init__(self):
        self.initialize()
        
    def initialize(self):
        '''
        Read settings from a file like grapetomato.config
        '''
        self.read_settings()

    def getTomato(self):
        return self.Tomato

    def getSBrake(self):
        return self.SBreak

    def getLBreak(self):
        return self.LBreak

    def setTomato(self, tomato):
        self.Tomato = tomato
    
    def setSBrake(self, sbreak):
        self.SBreak = sbreak
        
    def setLBreak(self, lbreak):
        self.LBreak = lbreak
        
    def update_settings(self, setting, value):
        pass
        
    def read_settings(self):
        #  read intervals
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(self.config_file)
        self.intervals_section = self.config_parser['Intervals']
        self.Tomato = int(self.intervals_section['tomato'])
        self.SBreak = int(self.intervals_section['small_break'])
        self.LBreak = int(self.intervals_section['large_break'])
