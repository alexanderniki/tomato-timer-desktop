from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon

from SysTrayMenu import SysTrayMenu

class TrayIcon(QSystemTrayIcon):
    def __init__(self, app_settings):
        super().__init__()

        self.settings = app_settings
        self.settings.TrayIcon = self
        print(self.settings.TrayIcon)

        self.setIcon(QIcon('res/ic_application.png'))
        self.setToolTip("Grape tomato")
        self.setContextMenu(SysTrayMenu(self.settings))

        self.activated.connect(self.showMainWindow)
        self.setVisible(True)
        self.showMessage('Hello', 'World', QSystemTrayIcon.MessageIcon(), 5000)

        self.show()

    def showMainWindow(self):
        self.settings.MainWindow.show()