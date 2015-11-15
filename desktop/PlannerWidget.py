from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer

from TimeoutMessageBox import TimeoutMessageBox


class PlannerWidget(QWidget):
    def __init__(self, app_settings):
        super().__init__()

        self.settings = app_settings
        self.settings.PlannerWidget = self
        if (self.settings.DEBUG == 1):
            print(self.settings.PlannerWidget)

        # Timer itself
        self.stopped = 1
        self.is_break = 0
        self.dot_visible = 1
        self.time_remaining = self.settings.Tomato
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reduceRemTime)
        self.current_seconds = 60
        self.seconds_timer = QTimer(self)
        self.seconds_timer.timeout.connect(self.blink)

        # Interval buttons. BTW, QPushButton has setFlat(bool) option
        # Tomato button:
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

        # Indicator dots:
        self.progress_indicator = QLabel(" : ")

        # Start/Stop button:
        self.startStopButton = QPushButton("Start")
        self.startStopButton.setToolTip("Start timer")
        self.startStopButton.clicked.connect(self.changeButtonState)

        # Layouts:
        self.time_button_box = QHBoxLayout()
        self.time_button_box.addWidget(self.tomato_button)
        self.time_button_box.addWidget(self.short_break_button)
        self.time_button_box.addWidget(self.long_break_button)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.currentTimeLabel)
        self.hbox.addWidget(self.progress_indicator)
        self.hbox.setAlignment(Qt.AlignCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.time_button_box)
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
            if (self.is_break == 0):
                self.settings.Tomatoes = self.settings.Tomatoes + 1
            self.stopTimer()
            self.message = TimeoutMessageBox()
            print("Tomatoes finished: " + str(self.settings.Tomatoes))
            self.settings.PlannerWindow.statusBar().showMessage(str(self.settings.Tomatoes) + ' tomatoes today')

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
        self.timer.start(60000) # Was 60000
        self.seconds_timer.start(500) # Was 1000
        print(str(self.time_remaining))
        self.updateTimeLabel(self.time_remaining)
        # Disable buttons while times is active:
        self.tomato_button.setDisabled(True)
        self.short_break_button.setDisabled(True)
        self.long_break_button.setDisabled(True)

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
        self.setTomato()

    def updateTimeLabel(self, value):
        if (value < 10):
            self.currentTimeLabel.setText("0" + str(value))
        else:
            self.currentTimeLabel.setText(str(value))

    def setShortBreak(self):
        if (self.timer.isActive()):
            self.short_break_button.setChecked(True)
        else:
            self.is_break = 1
            self.time_remaining = self.settings.SBreak
            self.updateTimeLabel(self.time_remaining)
            self.short_break_button.setChecked(True)
            self.tomato_button.setChecked(False)
            self.long_break_button.setChecked(False)

    def setLongBreak(self):
        if (self.timer.isActive()):
            self.long_break_button.setChecked(True)
        else:
            self.is_break = 1
            self.time_remaining = self.settings.LBreak
            self.updateTimeLabel(self.time_remaining)
            self.long_break_button.setChecked(True)
            self.tomato_button.setChecked(False)
            self.short_break_button.setChecked(False)

    def setTomato(self):
        if (self.timer.isActive()):
            self.tomato_button.setChecked(True)
        else:
            self.is_break = 0
            self.time_remaining = self.settings.Tomato
            self.updateTimeLabel(self.time_remaining)
            self.tomato_button.setChecked(True)
            self.short_break_button.setChecked(False)
            self.long_break_button.setChecked(False)

    def createTimeoutMessagebox(self):
        self.mbox_window = TimeoutMessageBox()

    def stopSecondsTimer(self):
        self.seconds_timer.stop()
        self.current_seconds = 60
        self.progress_indicator.setText(" : ")

    def blink(self):  # Show and hide dot or any other symbol near current time

        if (self.settings.DEBUG == 1):
            print("[LOG] blink()")  # Debug message

        if (self.dot_visible == 1):
            self.progress_indicator.setText("   ")
            self.dot_visible = 0
        else:
            self.progress_indicator.setText(" : ")
            self.dot_visible = 1
