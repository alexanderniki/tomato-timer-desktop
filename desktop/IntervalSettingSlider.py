from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class IntervalSettingSlider(QWidget):

    def __init__(self, app_settings, new_caption, new_value, interval_type):
        super().__init__()
        print("IntervalSettingsSlider: " + str(self))

        self.settings = app_settings
        self.settings.IntervalSettingSlider = self

        self.connected_interval = interval_type

        self.caption = new_caption
        self.caption_lbl = QLabel(self.caption)

        # Slider itself
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setValue(new_value)
        self.slider.valueChanged[int].connect(self.change_value)

        # Display value
        self.value_lbl = QLabel()
        self.value_lbl.setText(str(self.slider.value()))
        
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.caption_lbl)
        self.hbox.addWidget(self.slider)
        self.hbox.addWidget(self.value_lbl)

        self.setLayout(self.hbox)
        self.show()
        
    def get_caption(self):
        return self.caption
        
    def get_value(self):
        return self.value
        
    def set_caption(self, new_caption):
        self.caption = new_caption
        self.caption_lbl.setText(self.caption)
    
    def set_value(self, value):
        pass

    def set_maxvalue(self, value):
        self.slider.setMaximum(value)

    def set_minvalue(self, value):
        self.slider.setMinimum(value)

    def change_value(self):
        if (self.connected_interval == 'Tomato'):
            self.settings.setTomato(self.slider.value())
        else:
            if (self.connected_interval == 'SBreak'):
                self.settings.setSBreak(self.slider.value())
            else:
                if (self.connected_interval == 'LBreak'):
                    self.settings.setLBreak(self.slider.value())
        if self.slider.value() > 9:
            self.value_lbl.setText(str(self.slider.value()))
        else:  # if value contains of one symbol
            self.value_lbl.setText("0" + str(self.slider.value()))  # make it look like 01, 02,...,09
        print('Tomato: ' + str(self.settings.Tomato) + ', SBreak: ' + str(self.settings.SBreak) + ', LBreak: ' + str(self.settings.LBreak) )