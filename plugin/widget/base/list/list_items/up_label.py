from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class UpLabel(QWidget):

    def __init__(self, listWidget):

        super(UpLabel, self).__init__()

        self.list=listWidget

        layout, style_sheet=self.setUI()

        self.setLayout(layout)
        self.setStyleSheet(style_sheet)

    def setUI(self):

        style_sheet = '''
            QWidget{
                border-style: outset;
                border-width: 0px;
                border-radius: 5px;
                color: white;
                background-color: transparent;
                }
            QLabel{
                padding: 0px 10px 0px 10px;
                }
                '''

        self.up = QLabel()
        self.up.setWordWrap(True)

        self.up.hide()

        up_layout = QVBoxLayout()
        up_layout.setSpacing(0)
        up_layout.setContentsMargins(5, 5, 5, 5)

        up_layout.addWidget(self.up)
        up_layout.addStretch()

        return up_layout, style_sheet

    def setTextUp(self, text):

        self.up.setText(str(text))
        self.up.show()
        self.up.adjustSize()

    def textUp(self): return self.up.text()

    # def adjustSize(self):
    #     self.up.adjustSize()

    def setData(self, data):

        self.data=data
        if data.get('up', None):
            self.setTextUp(str(data.get('up')))
            color=data.get('up_color', None)
            if color: self.up.setStyleSheet(f'background-color: {color}')
        color=data.get('color', None)
        if color: self.setStyleSheet(f'background-color: {color}')
        self.adjustSize()

    def isin(self, text, data, fields):

        if text.lower() in data['up'].lower(): return True

    def setFixedWidth(self, width):

        super().setFixedWidth(width)#-20)
        self.up.setFixedWidth(width)#-20)
