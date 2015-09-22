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
        self.time_remaining = self.settings.Tomato
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reduceRemTime)
        self.current_seconds = 60
        self.seconds_timer = QTimer(self)
        self.seconds_timer.timeout.connect(self.reduceSeconds)

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

        self.hbox.addWidget(self.currentTimeLabel)
        self.hbox.addWidget(self.seconds_label)
        self.hbox.setAlignment(Qt.AlignCenter)
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
            self.stopTimer()
            self.message = TimeoutMessageBox()
            self.settings.Tomatoes = self.settings.Tomatoes + 1
            print("Tomatoes finished: " + str(self.settings.Tomatoes))
            self.settings.PlannerWindow.statusBar().showMessage(str(self.settings.Tomatoes) + ' tomatoes today')

    def changeButtonState(self):
        print("[LOG] changeButtonState()")
        if (self.stopped == 1):
            # Set correct minutes, since the timer works with seconds
            self.time_remaining = self.time_remaining - 1
            self.updateTimeLabel(self.time_remaining)
            self.updateSecondsLabel(59)

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
        self.seconds_timer.start(1000) # Was 1000
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