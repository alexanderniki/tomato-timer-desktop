from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

from PlannerWidget import PlannerWidget

class PlannerWindow(QMainWindow):
    def __init__(self, app_settings):
        super().__init__()

        self.settings = app_settings
        self.settings.PlannerWindow = self
        if (self.settings.DEBUG == 1):
            print(self.settings.PlannerWindow)

        self.setWindowTitle('Grape tomato') # Show window title
        self.setWindowIcon(QIcon('res/ic_application.png')) # Show window icon
        self.statusBar().showMessage(str(self.settings.Tomatoes) + ' tomatoes today') # Show status bar message

        self.plannerWidget = PlannerWidget(self.settings)

        self.setCentralWidget(self.plannerWidget)
        self.setFixedSize(240, 320) # Disable "Maximize" button

        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Active timer will be reset. <br /> Are you sure to quit? ", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()