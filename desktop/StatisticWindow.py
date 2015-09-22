from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QLabel

class StatisticWindow(QMainWindow):
    def __init__(self, app_settings):
        super().__init__()

        self.settings = app_settings
        self.settings.StatisticWindow = self
        print(self.settings.StatisticWindow)

        self.setWindowTitle('Statistic') # Show window title
        self.setWindowIcon(QIcon('ic_application.png')) # Show window icon
        self.statusBar().showMessage('Ready') # Show status bar message

        self.stat_widget = QWidget()
        self.tomatoes_amount = QLabel(self.stat_widget)
        self.tomatoes_amount.setText("Tomatoes finished: " + str(self.settings.Tomatoes))
        self.sbreaks_amount = QLabel(self.stat_widget)
        self.sbreaks_amount.setText("Short breaks finished: " + str(self.settings.SBreaks))
        self.lbreaks_amount = QLabel(self.stat_widget)
        self.lbreaks_amount.setText("Long breaks finished: " + str(self.settings.LBreaks))

        self.stat_widget_layout = QVBoxLayout()

        self.stat_widget_layout.addWidget(self.tomatoes_amount)
        self.stat_widget_layout.addWidget(self.sbreaks_amount)
        self.stat_widget_layout.addWidget(self.lbreaks_amount)
        self.stat_widget.setLayout(self.stat_widget_layout)

        # self.tomatoes_amount_text = QLabel("Tomatoes finished: " + str(tomatoes))
        # self.sbreaks_amount_text = QLabel("Short breaks finished: " + str(s_breaks))
        # self.lbreaks_amount_text = QLabel("Long breaks finished: " + str(l_breaks))
        self.setCentralWidget(self.stat_widget)

        self.show()