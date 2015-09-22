from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QWidget
from PyQt5.QtWidgets import QMessageBox, QToolBar, QPushButton
from PyQt5 import QtWidgets

from PlannerWidget import PlannerWidget
from AboutWindow import AboutWindow
from StatisticWindow import StatisticWindow
from MainMenu import MainMenu

class PlannerWindow(QMainWindow):
    def __init__(self, app_settings):
        super().__init__()

        self.settings = app_settings
        self.settings.PlannerWindow = self
        print(self.settings.PlannerWindow)

        self.use_menu = True

        self.setWindowTitle('Grape tomato') # Show window title
        self.setWindowIcon(QIcon('res/ic_application.png')) # Show window icon
        self.statusBar().showMessage('Ready') # Show status bar message

        self.plannerWidget = PlannerWidget(self.settings)

        # Actions for the menu: you actually can delete commented code
        # exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        # exit_action.setShortcut('Ctrl+Q')
        # exit_action.setStatusTip('Exit application')
        # exit_action.triggered.connect(qApp.quit)
        #
        # about_action = QAction(QIcon('exit.png'), '&About', self)
        # about_action.setShortcut('F1')
        # about_action.setStatusTip('About Grape tomato')
        # about_action.triggered.connect(self.showAboutWindow)
        #
        # statistic_action = QAction(QIcon('exit.png'), '&Statistic', self)
        # statistic_action.setStatusTip('Statistic')
        # statistic_action.triggered.connect(self.showStatisticWindow)

        if (self.use_menu):
            # Menu bar itself
            # self.menu_bar = self.menuBar()
            # self.menu = MainMenu(self.settings)
            # self.app_menu = self.menu_bar.addMenu(self.menu)
            #
            # self.menu.setStatusTip('Menu')
            pass

        else:
            # Toolbar with drop-down menu button
            # Button:
            self.menu_button = QPushButton()
            self.menu_button.setIcon(QIcon('res/ic_application.png'))
            self.menu_button.setMenu(MainMenu(self.settings))
            self.menu_button.setFlat(True)
            self.menu_button.setCheckable(True)
            self.menu_button.setFocusPolicy(Qt.NoFocus)
            # Horizontal spacer to move tool bar's button to the right
            self.h_spacer = QWidget()
            self.h_spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            # Toolbar:
            self.toolbar = QToolBar()
            self.toolbar.setFloatable(False)
            self.toolbar.setMovable(False)
            self.toolbar.addWidget(self.h_spacer)
            self.toolbar.addWidget(self.menu_button)
            self.main_toolbar = self.addToolBar(self.toolbar)

        self.setCentralWidget(self.plannerWidget)
        self.setFixedSize(240, 320) # Disable "Maximize" button

        self.show()

    def showAboutWindow(self):
        self.about_window = AboutWindow()

    def showStatisticWindow(self):
        self.statistic_window = StatisticWindow(self.settings)

    def closeEvent(self, event):
        self.minimize_to_tray = False # todo: move this setting to AppSettings
        if (self.minimize_to_tray):
            event.ignore()
            self.hide()
        else:
            reply = QMessageBox.question(self, 'Message',
                "Active timer will be reset. <br /> Are you sure to quit? ", QMessageBox.Yes |
                QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()