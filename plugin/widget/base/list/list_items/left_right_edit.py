from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class LeftRightEdit (QWidget):

    def __init__(self, listWidget):

        super(LeftRightEdit, self).__init__()

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

        left_right_layout = QHBoxLayout()
        left_right_layout.setSpacing(0)
        left_right_layout.setContentsMargins(0, 10, 0, 10)

        self.left = QLabel(objectName='leftLabel')
        self.left.setWordWrap(True)

        self.right = QPlainTextEdit(objectName='rightEdit')
        self.right.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.right.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.right.textChanged.connect(self.on_contentChanged)

        left_right_layout.addWidget(self.left)
        left_right_layout.addWidget(self.right)
        left_right_layout.addStretch(1)

        return left_right_layout, style_sheet

    def setTextRight(self, text):

        self.right.setPlainText(text)
        self.adjustSize()

    def setTextLeft(self, text):

        self.left.setText(text)
        self.left.adjustSize()

    def textLeft(self):

        return self.left.text()

    def textRight(self):

        return self.right.toPlainText()

    def adjustSize(self):

        # self.left.adjustSize()
        self.right.adjustSize()

    def getRightSize(self):

        size=self.right.document().size()
        width=int(size.width())
        if size.height()==1.0:
            times=int(width/self.right.size().width())
        else:
            times=size.height()
        if times==0: times=1
        height=int(25*times)
        if height<50: height=50
        size=QSize(width, height)
        return size

    def setFixedWidth(self, width):

        super().setFixedWidth(width)
        self.left.adjustSize()
        substract=0
        if self.left.isVisible():
            substract+=self.left.size().width()
            substract+=30 # padding
        self.right.setFixedWidth(width-substract)
        self.right.setFixedHeight(self.getRightSize().height())

    def setData(self, data):

        self.data=data
        if data.get('left', None):
            self.setTextLeft(str(data.get('left')))
            color=data.get('left_color', None)
            if color: 
                self.left.setStyleSheet(f'background-color: {color}; color: black;')
        if data.get('right', None):
            self.setTextRight(str(data.get('right')))
            color=data.get('left_color', None)
            if color: 
                self.left.setStyleSheet(f'background-color: {color}; color: black;')
        self.adjustSize()

    def isin(self, text, data, fields):
        conditions=[]
        for f in fields:
            field_text= str(data.get(f, ''))
            if field_text and text.lower() in field_text.lower():
                return True
        return False

    def setFocus(self):

        self.right.setFocus()

    def on_contentChanged(self):

        self.list.widgetDataChanged.emit(self)

    def installEventFilter(self, listener):

        self.left.installEventFilter(listener)
        self.right.installEventFilter(listener)
