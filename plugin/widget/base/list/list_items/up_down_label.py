from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class UpDownLabel(QWidget):

    def __init__(self, listWidget):

        super(UpDownLabel, self).__init__()

        self.list=listWidget

        layout, style_sheet=self.setUI()

        self.setLayout(layout)
        self.setStyleSheet(style_sheet)

    def setUI(self):

        style_sheet = '''

            QWidget{
                border-style: outset;
                border-width: 0px;
                border-radius: 10px;
                color: white;
                }

            QLabel{
                padding: 0px 5px 0px 5px;
                }

                '''

        self.up = QLabel()
        self.down = QLabel()

        self.up.setWordWrap(True)
        self.down.setWordWrap(True)

        self.up.hide()
        self.down.hide()

        up_down_layout = QVBoxLayout()
        up_down_layout.setSpacing(0)
        up_down_layout.setContentsMargins(0, 0, 0, 0)

        up_down_layout.addWidget(self.up, 50)
        up_down_layout.addWidget(self.down, 50)

        up_down_layout.addStretch()

        return up_down_layout, style_sheet

    def setTextDown(self, text):

        self.down.setText(str(text))
        self.down.show()
        self.down.adjustSize()

    def setTextUp(self, text):

        self.up.setText(str(text))
        self.up.show()
        self.up.adjustSize()

    def textUp(self): return self.up.text()

    def textDown(self): return self.down.text()

    def setData(self, data):

        self.data=data
        if data.get('up', None):
            self.setTextUp(str(data.get('up')))
            color=data.get('up_color', None)
            if color: 
                self.up.setStyleSheet(f'background-color: {color}; color: black;')
        if data.get('down', None):
            self.setTextDown(str(data.get('down')))
            color=data.get('up_color', None)
            if color: 
                self.up.setStyleSheet(f'background-color: {color}; color: black;')

    def isin(self, text, data, fields):

        conditions=[]

        for f in fields:
            field_text= str(data.get(f, ''))
            if field_text and text.lower() in field_text.lower():
                conditions+=[True]
            else:
                conditions+=[False]
        return any(conditions)

    def setFixedWidth(self, width):

        super().setFixedWidth(width)
        self.up.setFixedWidth(width)
        self.down.setFixedWidth(width)

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        self.up.installEventFilter(listener)
        self.down.installEventFilter(listener)
