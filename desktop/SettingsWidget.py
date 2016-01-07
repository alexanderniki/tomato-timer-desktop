from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from IntervalSettingSlider import IntervalSettingSlider


class SettingsWidget(QWidget):
    def __init__(self, app_settings):
        super().__init__()


        self.settings = app_settings
        self.settings.SettingsWidget = self
        if (self.settings.DEBUG == 1):
            print("Creating SettingsWidget ...")
            print(self.settings.SettingsWidget)

        self.tomato_interval = IntervalSettingSlider(self.settings, "Tomato:", self.settings.Tomato, 'Tomato')
        self.tomato_interval.set_maxvalue(90)
        self.sb_interval = IntervalSettingSlider(self.settings, "Short break:", self.settings.SBreak, 'SBreak')
        self.sb_interval.set_maxvalue(30)
        self.lb_interval = IntervalSettingSlider(self.settings, "Long break:", self.settings.LBreak, 'LBreak')
        self.lb_interval.set_maxvalue(60)

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.settings.update_settings)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tomato_interval)
        self.vbox.addWidget(self.sb_interval)
        self.vbox.addWidget(self.lb_interval)
        self.vbox.addWidget(self.apply_button)
        self.setLayout(self.vbox)

        #  self.settings.update_settings()

        self.show()
