from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QAction, qApp
from PyQt5.QtWidgets import  QMenu

from AboutWindow import AboutWindow
from StatisticWindow import StatisticWindow

class MainMenu(QMenu):
    def __init__(self, app_settings):
        super().__init__()

        self.settings = app_settings
        self.settings.MainMenu = self

        # Actions for the menu
        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)

        about_action = QAction(QIcon('exit.png'), '&About', self)
        about_action.setShortcut('F1')
        about_action.setStatusTip('About Grape tomato')
        about_action.triggered.connect(self.showAboutWindow)

        statistic_action = QAction(QIcon('exit.png'), '&Statistic', self)
        statistic_action.setStatusTip('Statistic')
        statistic_action.triggered.connect(self.showStatisticWindow)

        # Create menu
        self.addAction(statistic_action)
        self.addSeparator()
        self.addAction(about_action)
        self.addAction(exit_action)

        self.setTitle('Menu')

    def showAboutWindow(self):
        self.about_window = AboutWindow(self.settings)

    def showStatisticWindow(self):
        self.statistic_window = StatisticWindow(self.settings)