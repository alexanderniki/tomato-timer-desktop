import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from SettingsWidget import SettingsWidget


class SettingsWindow(QMainWindow):
    def __init__(self, app_settings):
        super().__init__()

        # Get settings and register this window into them
        # Получаем настройки и регистрируем в них свое окно
        self.settings = app_settings
        self.settings.SettingsWindow = self
        if (self.settings.DEBUG == 1):
            print("Creating SettingsWindow ...")
            print(self.settings.SettingsWindow)

        # Get current dir
        # Получаем директорию, в которой работает приложение
        app_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        if (self.settings.DEBUG == 1):
            print("App path is: " + app_path)

        self.setWindowTitle('Settings') # Show window title
        self.setWindowIcon(QIcon(app_path + "/res/ic_application.png"))  # Show window icon
        self.statusBar().showMessage("Settings")  # Show status bar message

        self.settings_widget = SettingsWidget(self.settings)
        self.setCentralWidget(self.settings_widget)

        self.show()
