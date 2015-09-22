import sys
from PyQt5.QtWidgets import  QMenu
from AboutWindow import AboutWindow
from StatisticWindow import StatisticWindow

class SysTrayMenu(QMenu):
    def __init__(self, app_settings):
        super().__init__()

        self.settings = app_settings
        self.settings.SysTrayMenu = self

        self.item_exit = self.addAction("Exit")
        self.item_exit.triggered.connect(sys.exit)

        self.item_about = self.addAction("About Grape Tomato")
        self.item_about.triggered.connect(self.showAboutWindow)

        self.item_statistic = self.addAction("Statistic")
        self.item_statistic.triggered.connect(self.showStatisticWindow)

    def showAboutWindow(self):
        self.about_window = AboutWindow()

    def showStatisticWindow(self):
        # tomatoes = self.app_window.planner.tomatoes_per_session
        # l_breaks = self.app_window.planner.lbreaks_per_session
        # s_breaks = self.app_window.planner.sbreaks_per_session
        # self.statistic_window = StatisticWindow(tomatoes, s_breaks, l_breaks)
        pass

