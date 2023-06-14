from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Item(QWidget):

    def __init__(self, listWidget):

        super(Item, self).__init__()

        self.list=listWidget

        layout, style_sheet=self.setUI()

        self.setLayout(layout)
        self.setStyleSheet(style_sheet)

    def setUI(self):

        style_sheet = '''

            QWidget{
                border-width: 0px;
                color: white;
                }
            QLabel{
                padding: 0px 10px 0px 10px;
                }
                '''

        self.up = QLabel(objectName='upLabel')
        self.up.setWordWrap(True)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.addWidget(self.up)

        return layout, style_sheet

    def setTextUp(self, text):

        self.up.setText(str(text))
        self.up.show()
        self.up.adjustSize()

    def textUp(self): return self.up.text()

    def setData(self, data):

        self.data=data
        if data.get('up', None):
            self.setTextUp(str(data.get('up')))
            color=data.get('up_color', None)
            if color: 
                self.setStyleSheet(' '.join(
                    ['QLabel#upLabel{',
                     f'background-color: {color};',
                     'color: black;',
                     'padding: 0px 10px 0px 10px;}'
                     ]))

        color=data.get('color', None)
        if color: 
            self.setStyleSheet(
                    f'background-color: {color}; color: black;')

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
        width-=10 # padding
        self.up.setFixedWidth(width)

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        self.up.installEventFilter(listener)
