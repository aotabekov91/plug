from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class UpLabel(QWidget):
    def __init__(self, parent=None):
        super(UpLabel, self).__init__(parent)

        layout, style_sheet=self.setUI()

        self.setLayout(layout)
        self.setStyleSheet(style_sheet)

    def setUI(self):
        style_sheet = '''
            QWidget{
                border-style: outset;
                border-width: 0px;
                border-radius: 5px;
                color: grey;
                }
            QLabel{
                padding: 0px 0px 0px 10px;
                }
                '''

        self.up = QLabel()
        self.up.setWordWrap(True)

        self.up.hide()

        up_layout = QVBoxLayout()
        up_layout.setSpacing(0)
        up_layout.setContentsMargins(0, 10, 0, 10)

        up_layout.addWidget(self.up)
        up_layout.addStretch()

        return up_layout, style_sheet

    def setTextUp(self, text):
        self.up.setText(str(text))
        self.up.show()
        self.up.adjustSize()

    def textUp(self):
        return self.up.text()

    def adjustSize(self):
        self.up.adjustSize()

    def sizeHint(self):
        self.adjustSize()
        size=self.up.size()
        size.setHeight(size.height()+20)
        if size.height()<30:
            size.setHeight(30)
        return size

    def setData(self, data):
        self.data=data
        if data.get('up', None):
            self.setTextUp(str(data.get('up')))
            color=data.get('up_color', None)
            if color: self.up.setStyleSheet(f'background-color: {color}')
        self.adjustSize()

    def isCompatible(self, text, data):
        text_up = data.get('top', '')

        cond1 = text_up and text.lower() in str(text_up).lower() 
        if cond1:
            return True
        else:
            return False

    def setFixedWidth(self, width):
        super().setFixedWidth(width)
        self.up.setFixedWidth(width)
