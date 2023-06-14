import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .up_down_label import UpDownLabel

class IconUpDown (UpDownLabel):

    def setUI(self):

        up_down_layout, style_sheet=super().setUI()

        style_sheet += '''

            QWidget#iconTextContainer{
                border-style: outset;
                border-width: 0px;
                border-radius: 10px;
                color: transparent;
                background-color: transparent;
                }
            QLabel#iconLabel{
                padding: 0 0 0 0;
                background-color: transparent;
                }

                '''

        self.icon = QLabel(objectName='iconLabel')
        self.icon.setFixedWidth(int(0.15*self.size().width()))

        self.icon.hide()

        up_down_container=QWidget(objectName='upDownContainer')
        up_down_container.setLayout(up_down_layout)

        icon_text_layout = QHBoxLayout()
        icon_text_layout.setSpacing(0)
        icon_text_layout.addWidget(self.icon)
        icon_text_layout.addWidget(up_down_container)

        icon_text_container=QWidget(objectName='iconTextContainer')
        icon_text_container.setLayout(icon_text_layout)

        layout=QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(icon_text_container)

        return layout, style_sheet

    def setIcon(self, imagePath):

        self.icon.path = imagePath
        if os.path.isfile(imagePath):
            scale=self.icon.size()
            w, h=scale.width(), scale.height()
            self.icon.setPixmap(QPixmap(imagePath).scaled(w, h, Qt.KeepAspectRatio))
            self.icon.show()

    def setData(self, data):

        super().setData(data)
        if data.get('icon', False):
            self.setIcon(data['icon'])

    def setFixedWidth(self, width):

        super().setFixedWidth(width)
        substract=20
        if self.icon.isVisible():
            substract+=40 # icon padding
            substract+=self.icon.size().width()
        width-=substract
        self.up.setFixedWidth(width)
        self.down.setFixedWidth(width)
