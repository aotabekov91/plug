from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class UpDownEdit (QWidget):

    def __init__(self, listWidget):

        super(UpDownEdit, self).__init__()

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
                background-color: transparent;
                }
            QLabel{
                padding: 0px 10px 0px 10px;
                }
            QPlainTextEdit{
                padding: 0px 10px 0px 10px;
                }
                '''

        up_down_layout = QVBoxLayout()
        up_down_layout.setSpacing(0)
        up_down_layout.setContentsMargins(0, 10, 0, 10)

        self.up = QLabel(objectName='upLabel')
        self.up.setWordWrap(True)

        self.down = QPlainTextEdit(objectName='downEdit')
        self.down.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.down.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.down.textChanged.connect(self.on_contentChanged)

        up_down_layout.setSpacing(0)
        up_down_layout.addWidget(self.up, 30)
        up_down_layout.addWidget(self.down, 70)
        up_down_layout.addStretch(1)

        return up_down_layout, style_sheet

    def setTextDown(self, text):

        self.down.setPlainText(text)
        self.down.show()
        self.adjustSize()

    def setTextUp(self, text):

        self.up.setText(text)
        self.up.show()
        self.up.adjustSize()

    def textUp(self):

        return self.up.text()

    def textDown(self):

        return self.down.toPlainText()

    def adjustSize(self):

        self.up.adjustSize()
        self.down.adjustSize()

    def getDownSize(self):

        size=self.down.document().size()
        width=int(size.width())
        if size.height()==1.0:
            times=int(width/self.down.size().width())
        else:
            times=size.height()
        if times==0: times=1
        height=int(25*times)
        if height<50: height=50
        size=QSize(width, height)
        return size

    def setFixedWidth(self, width):

        super().setFixedWidth(width)
        self.up.setFixedWidth(width)
        self.down.setFixedWidth(width)
        self.down.setFixedHeight(self.getDownSize().height())

    def sizeHint(self):

        self.adjustSize()
        size=self.up.size()
        s=self.getDownSize()
        # s=self.down.size()
        size.setHeight(int(size.height()+s.height()+15))
        return size

    def setData(self, data):

        self.data=data
        if data.get('up', None):
            self.setTextUp(str(data.get('up')))
            color=data.get('up_color', None)
            if color: self.up.setStyleSheet(f'background-color: {color}; color: black;')
        if data.get('down', None):
            self.setTextDown(str(data.get('down')))
            color=data.get('up_color', None)
            if color: self.up.setStyleSheet(f'background-color: {color}; color: black;')
        self.adjustSize()

    def isin(self, text, data, fields):

        for f in fields:
            field_text= str(data.get(f, ''))
            if field_text and text.lower() in field_text.lower(): 
                return True
        return False

    def on_contentChanged(self):

        self.list.widgetDataChanged.emit(self)

    def setFocus(self):

        self.down.setFocus()

    def installEventFilter(self, listener):

        self.up.installEventFilter(listener)
        self.down.installEventFilter(listener)
