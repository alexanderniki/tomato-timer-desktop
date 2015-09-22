from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets

from TimeoutMessageBox import TimeoutMessageBox
from StatisticWindow import StatisticWindow
from MainMenu import MainMenu
from TrayIcon import  TrayIcon

class PlannerWidget(QWidget):
    def __init__(self, app_settings):
        super().__init__()

        self.settings = app_settings
        self.settings.PlannerWidget = self
        print(self.settings.PlannerWidget)

        self.useComboTimes = False

        # Timer itself
        self.stopped = 1
        self.time_remaining = self.settings.Tomato
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reduceRemTime)
        self.current_seconds = 60
        self.seconds_timer = QTimer(self)
        self.seconds_timer.timeout.connect(self.reduceSeconds)

        # Custom menu button
        self.menu_button_t = QPushButton(self)
        self.menu_button_t.setIcon(QIcon('res/ic_application.png'))
        self.menu_button_t.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.menu_button_t.setFlat(True)
        self.menu_button_t.setFocusPolicy(Qt.NoFocus)
        self.menu_button_t.setMenu(MainMenu(self.settings))
        self.h_separator = QWidget()
        self.h_separator.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.h_toolbox_layout = QHBoxLayout()
        self.h_toolbox_layout.setAlignment(Qt.AlignLeft)
        self.h_toolbox_layout.addWidget(self.menu_button_t)
        #self.h_toolbox_layout.addWidget(self.h_separator)

        # Interval buttons. BTW, QPushButton has setFlat(bool) option
        # Tomato:
        self.tomato_button = QPushButton("Tomato")
        self.tomato_button.setCheckable(True)
        self.tomato_button.setChecked(True)
        self.tomato_button.clicked.connect(self.setTomato)
        # Short break button:
        self.short_break_button = QPushButton("S-break")
        self.short_break_button.setCheckable(True)
        self.short_break_button.clicked.connect(self.setShortBreak)
        # Long break button:
        self.long_break_button = QPushButton("L- break")
        self.long_break_button.setCheckable(True)
        self.long_break_button.clicked.connect(self.setLongBreak)

        # Time label:
        self.currentTimeLabel = QLabel(str(self.time_remaining), self)
        self.currentTimeLabel.setStyleSheet("QWidget { color: #424242; font-size: 72px;  }")
        self.seconds_label = QLabel(': 00')
        # Start/Stop button:
        self.startStopButton = QPushButton("Start")
        self.startStopButton.setToolTip("Start timer")
        self.startStopButton.clicked.connect(self.changeButtonState)

        # Layouts:
        self.time_button_box = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        self.time_button_box.addWidget(self.tomato_button)
        self.time_button_box.addWidget(self.short_break_button)
        self.time_button_box.addWidget(self.long_break_button)
        # Experimental menu button
        self.vbox.addLayout(self.h_toolbox_layout)
        if (self.useComboTimes): # If you would like to choose intervals from combo box
            # Combo box with time intervals:
            self.time_combo = QComboBox(self)
            self.time_combo.addItem('Tomato')
            self.time_combo.addItem('Short break')
            self.time_combo.addItem('Long break')
            self.vbox.addWidget(self.time_combo)
        else: # Or, when you'd like to use classic buttons
            self.vbox.addLayout(self.time_button_box)

        self.hbox.addWidget(self.currentTimeLabel)
        self.hbox.addWidget(self.seconds_label)
        self.hbox.setAlignment(Qt.AlignCenter)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.startStopButton)

        self.setLayout(self.vbox)
        self.show()

    def reduceRemTime(self):
        print("[LOG] reduceRemTime()")
        self.time_remaining = self.time_remaining - 1
        if (self.time_remaining > 0):
            self.startTomatoTimer()
        else:
            self.stopTimer()
            self.message = TimeoutMessageBox() # Commented because this particular code is the reason of the error with threads.
            self.settings.Tomatoes = self.settings.Tomatoes + 1
            print("Tomatoes finished: " + str(self.settings.Tomatoes))

    def changeButtonState(self):
        print("[LOG] changeButtonState()")
        if (self.stopped == 1):
            self.startTomatoTimer()
            self.startStopButton.setText('Stop')
            self.startStopButton.setToolTip("Stop timer")
            # todo: change status bar text (ask somebody about how to do that)
        else:
            self.stopTimer()
            self.startStopButton.setText('Start')
            self.startStopButton.setToolTip("Start timer")
            # todo: change status bar text (ask somebody about how to do that)

    def startTomatoTimer(self):
        print("[LOG] startTomatoTimer()" )
        if (self.stopped == 1):
             print('Started')
        self.stopped = 0
        self.timer.start(60000)
        self.seconds_timer.start(1000)
        print(str(self.time_remaining))
        self.updateTimeLabel(self.time_remaining)
        # Disable buttons while times is active:
        self.tomato_button.setDisabled(True)
        self.short_break_button.setDisabled(True)
        self.long_break_button.setDisabled(True)
        #self.currentTimeLabel.setStyleSheet("QWidget { color: #307730; font-size: 72px;  }")

    def stopTimer(self):
        print("[LOG] stopTimer")
        if self.timer.isActive():
            self.timer.stop()
            self.stopSecondsTimer()
        self.stopped = 1
        self.time_remaining = self.settings.Tomato
        print('Stopped')
        self.updateTimeLabel(self.time_remaining)
        self.startStopButton.setText('Start')
        self.startStopButton.setToolTip("Start timer")
        # Enable buttons, when timer stopped:
        self.tomato_button.setEnabled(True)
        self.short_break_button.setEnabled(True)
        self.long_break_button.setEnabled(True)

    def updateTimeLabel(self, value):
        self.currentTimeLabel.setText(str(value))

    def setShortBreak(self):
        if (self.timer.isActive()):
            self.short_break_button.setChecked(True)
        else:
            self.time_remaining = self.settings.SBreak
            self.updateTimeLabel(self.time_remaining)
            self.short_break_button.setChecked(True)
            self.tomato_button.setChecked(False)
            self.long_break_button.setChecked(False)

    def setLongBreak(self):
        if (self.timer.isActive()):
            self.long_break_button.setChecked(True)
        else:
            self.time_remaining = self.settings.LBreak
            self.updateTimeLabel(self.time_remaining)
            self.long_break_button.setChecked(True)
            self.tomato_button.setChecked(False)
            self.short_break_button.setChecked(False)

    def setTomato(self):
        if (self.timer.isActive()):
            self.tomato_button.setChecked(True)
        else:
            self.time_remaining = self.settings.Tomato
            self.updateTimeLabel(self.time_remaining)
            self.tomato_button.setChecked(True)
            self.short_break_button.setChecked(False)
            self.long_break_button.setChecked(False)

    def createTimeoutMessagebox(self):
        self.mbox_window = TimeoutMessageBox()

    def showAboutWindow(self):
        self.about_window = AboutWindow()

    def showStatisticWindow(self):
        self.statistic_window = StatisticWindow()

    def reduceSeconds(self):
        if (self.current_seconds > 0):
            print(str(self.current_seconds))
            self.current_seconds = self.current_seconds - 1
            self.updateSecondsLabel(self.current_seconds)
        else:
            self.current_seconds = 59
            self.updateSecondsLabel(self.current_seconds)

    def updateSecondsLabel(self, value):
        if (value > 9):
            self.seconds_label.setText(': ' + str(value))
        else:
            # Place 0 before value to avoid a little layout collapse so it would look like ": 09-08-07-etc"
            self.seconds_label.setText(': 0' + str(value))

    def stopSecondsTimer(self):
        self.seconds_timer.stop()
        self.updateSecondsLabel(00)
        self.current_seconds = 60