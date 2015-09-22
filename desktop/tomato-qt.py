'''
Grape Tomato:
Simple tomato timer/planner application
version: 0.1.1
'''

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QAction, qApp
from PyQt5.QtWidgets import QLabel, QPushButton, QSystemTrayIcon, QMessageBox, QMenu
from PyQt5.QtCore import QTime, QTimer


class Tomato:
    pomodoro_interval = 25 # 25 minutes
    short_break = 5 # 5 minutes
    long_break = 15 # 15 minutes
    
    tomatoes_per_session = 0 # starting with 0 completed tomatoes
    lbreaks_per_session = 0 # Starting with 0 completed long breaks
    sbreaks_per_session = 0 # Starting with 0 completed short breaks


class PlannerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Grape tomato') # Show window title
        self.setWindowIcon(QIcon('ic_application.png')) # Show window icon
        self.statusBar().showMessage('Ready') # Show status bar message

        self.trayIcon = TrayIcon()
        self.plannerWidget = PlannerWidget()

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

        self.menu_bar = self.menuBar()
        self.testmenu = SysTrayMenu()
        self.menu_bar.addMenu(self.testmenu)
        self.menu = self.menu_bar.addMenu('&Menu')
        self.menu.addAction(statistic_action)
        self.menu.addAction(about_action)
        self.menu.addAction(exit_action)

        self.setCentralWidget(self.plannerWidget)
        self.setFixedSize(240, 320) # Disable "Maximize" button

        self.show()

    def showAboutWindow(self):
        self.about_window = AboutWindow()

    def showStatisticWindow(self):
        tomatoes = self.plannerWidget.planner.tomatoes_per_session
        l_breaks = self.plannerWidget.planner.lbreaks_per_session
        s_breaks = self.plannerWidget.planner.sbreaks_per_session
        self.statistic_window = StatisticWindow(tomatoes, s_breaks, l_breaks)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Active timer will be reset. <br /> Are you sure to quit? ", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class TrayIcon(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        # self.menu = QMenu()
        # self.item_exit = self.menu.addAction("Exit")
        # self.item_exit.triggered.connect(sys.exit)

        self.menu = SysTrayMenu()
        self.setIcon(QIcon('ic_application.png'))
        self.setToolTip("Grape tomato")
        self.setContextMenu(self.menu)
        self.setVisible(1)
        self.show()

class SysTrayMenu(QMenu):
    def __init__(self):
        super().__init__()

        self.item_exit = self.addAction("Exit")
        self.item_exit.triggered.connect(sys.exit)

        self.item_about = self.addAction("About Grape Tomato")
        self.item_about.triggered.connect(self.showAboutWindow)

        self.item_statistic = self.addAction("Statistic")
        self.item_statistic.triggered.connect(self.showStatisticWindow)

    def showAboutWindow(self):
        self.about_window = AboutWindow()

    def showStatisticWindow(self):
        pass


class PlannerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.planner = Tomato()

        # Timer itself
        self.stopped = 1
        self.time_remaining = self.planner.pomodoro_interval
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reduceRemTime)

        # Interval buttons
        self.tomato_button = QPushButton("Tomato")
        self.tomato_button.setCheckable(True)
        self.tomato_button.setChecked(True)
        self.tomato_button.clicked.connect(self.setTomato)
        self.short_break_button = QPushButton("S-break")
        self.short_break_button.setCheckable(True)
        self.short_break_button.clicked.connect(self.setShortBreak)
        self.long_break_button = QPushButton("L- break")
        self.long_break_button.setCheckable(True)
        self.long_break_button.clicked.connect(self.setLongBreak)

        # Time label:
        self.currentTimeLabel = QLabel(str(self.time_remaining), self)
        self.currentTimeLabel.setStyleSheet("QWidget { color: #424242; font-size: 72px;  }")
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
        self.vbox.addLayout(self.time_button_box)

        self.hbox.addWidget(self.currentTimeLabel)
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
            self.planner.tomatoes_per_session = self.planner.tomatoes_per_session + 1
            print("Tomatoes finished: " + str(self.planner.tomatoes_per_session))

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
        print(str(self.time_remaining))
        self.updateTimeLabel(self.time_remaining)

    def stopTimer(self):
        print("[LOG] stopTimer")
        if self.timer.isActive():
            self.timer.stop()
        self.stopped = 1
        self.time_remaining = self.planner.pomodoro_interval
        print('Stopped')
        self.updateTimeLabel(self.time_remaining)
        self.startStopButton.setText('Start')
        self.startStopButton.setToolTip("Start timer")

    def updateTimeLabel(self, value):
        self.currentTimeLabel.setText(str(value))

    def setShortBreak(self):
        if (self.timer.isActive()):
            self.short_break_button.setChecked(True)
        else:
            self.time_remaining = self.planner.short_break
            self.updateTimeLabel(self.time_remaining)
            self.tomato_button.setChecked(False)
            self.long_break_button.setChecked(False)

    def setLongBreak(self):
        if (self.timer.isActive()):
            self.long_break_button.setChecked(True)
        else:
            self.time_remaining = self.planner.long_break
            self.updateTimeLabel(self.time_remaining)
            self.tomato_button.setChecked(False)
            self.short_break_button.setChecked(False)

    def setTomato(self):
        if (self.timer.isActive()):
            self.tomato_button.setChecked(True)
        else:
            self.time_remaining = self.planner.pomodoro_interval
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


class TimeoutMessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.information(self, "Tomato finished!", "You have finished the tomato.")


class PlannerApp(QApplication):
    # I don't use this class yet. If I do, the app crashes with error:
    # *** Error in `/usr/bin/python3.4': double free or corruption (!prev): 0x0000000001e67010 ***
    def __init__(self):
        super().__init__(sys.argv)
        self.window = PlannerWindow()


class AboutWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('About Tomato planner') # Show window title
        self.setWindowIcon(QIcon('ic_application.png')) # Show window icon
        self.statusBar().showMessage('Ready') # Show status bar message

        self.about_text = QLabel("Tomato planner app")
        self.setCentralWidget(self.about_text)

        self.show()

class StatisticWindow(QMainWindow):
    def __init__(self, tomatoes, s_breaks, l_breaks):
        super().__init__()

        self.setWindowTitle('Statistic') # Show window title
        self.setWindowIcon(QIcon('ic_application.png')) # Show window icon
        self.statusBar().showMessage('Ready') # Show status bar message

        self.stat_widget = QWidget()
        self.tomatoes_amount = QLabel(self.stat_widget)
        self.tomatoes_amount.setText("Tomatoes finished: " + str(tomatoes))
        self.sbreaks_amount = QLabel(self.stat_widget)
        self.sbreaks_amount.setText("Short breaks finished: " + str(s_breaks))
        self.lbreaks_amount = QLabel(self.stat_widget)
        self.lbreaks_amount.setText("Long breaks finished: " + str(l_breaks))

        self.stat_widget_layout = QVBoxLayout()

        self.stat_widget_layout.addWidget(self.tomatoes_amount)
        self.stat_widget_layout.addWidget(self.sbreaks_amount)
        self.stat_widget_layout.addWidget(self.lbreaks_amount)
        self.stat_widget.setLayout(self.stat_widget_layout)

        self.tomatoes_amount_text = QLabel("Tomatoes finished: " + str(tomatoes))
        self.sbreaks_amount_text = QLabel("Short breaks finished: " + str(s_breaks))
        self.lbreaks_amount_text = QLabel("Long breaks finished: " + str(l_breaks))
        self.setCentralWidget(self.stat_widget)

        self.show()


def main():
    app = QApplication(sys.argv)
    ex = PlannerWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
