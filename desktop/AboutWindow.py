from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QWidget

class AboutWindow(QMainWindow):
    def __init__(self, app_settings):
        super().__init__()

        self.settings = app_settings
        self.settings.AboutWindow = self
        print(self.settings.AboutWindow)

        self.setWindowTitle('About Grape Tomato') # Show window title
        self.setWindowIcon(QIcon('ic_application.png')) # Show window icon
        self.statusBar().showMessage('Ready') # Show status bar message

        self.about_text = QLabel("Tomato planner app")
        self.setCentralWidget(self.about_text)

        self.show()