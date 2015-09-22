class AppSettings:
    
    # Tomato settings:
    Tomato = 25
    SBreak = 5
    LBreak = 15
    
    # Statistic settings:
    Tomatoes = 0
    SBreaks = 0
    LBreaks = 0
    
    # Application:
    MainWindow = None
    TrayIcon = None
    AboutWindow = None
    PlannerWindow = None
    SettingsWindow = None
    StatisticWindow = None
    SysTrayMenu = None
    MainMenu = None

    def __init__(self):
        self.initialize()
        
    def initialize(self):
        pass

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