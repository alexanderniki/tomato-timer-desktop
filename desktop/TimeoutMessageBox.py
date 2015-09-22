from PyQt5.QtWidgets import QMessageBox


class TimeoutMessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.information(self, "Tomato finished!", "You have finished the tomato.")