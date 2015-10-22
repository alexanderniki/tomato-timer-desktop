'''
Grape Tomato:
Simple tomato timer/planner application
version: 0.2.0
'''

import sys
from PyQt5.QtWidgets import QApplication
from PlannerWindow import PlannerWindow
import AppSettings


class PlannerApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.settings = AppSettings.AppSettings()
        self.window = PlannerWindow(self.settings)

def main():
    app = PlannerApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
