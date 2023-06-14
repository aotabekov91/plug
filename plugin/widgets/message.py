import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..base import key
from .components import MainWindow

class MessageWindow(MainWindow):

    messageHidden=pyqtSignal()

    def __init__ (self, app, window_title='Notification', label_title=''):

        super(MessageWindow, self).__init__(app, window_title)

        self.pause=False
        self.setMinimumWidth(300)

        self.style_sheet='''
            QWidget{
                font-size: 18px;
                color: white;
                padding: 10px 10px 10px 10px;
                border-color: transparent;
                background-color: transparent;
                }
            QWidget#main{
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: red;
                background-color: #101010;
                }
            QLabel{
                color: white;
                background-color: green;
                border-width: 0px
                border-color: transparent;
                }
                '''

        self.main = QWidget(objectName='main')

        self.title=QLabel()
        self.title.setWordWrap(True)
        self.information=QLabel()
        self.information.setWordWrap(True)
        self.detail=QLabel()
        self.detail.setWordWrap(True)

        self.title.hide()
        self.information.hide()
        self.detail.hide()

        layout=QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        layout.addWidget(self.title, 10)
        layout.addWidget(self.information, 50)
        layout.addWidget(self.detail, 40)
        layout.addStretch(1)

        self.main.setLayout(layout)
        self.main.adjustSize()

        self.main.setStyleSheet(self.style_sheet)
        self.setCentralWidget(self.main)

    def setTitle(self, text):
        text=text.strip().title()
        self.title.setText(text)
        self.title.adjustSize()
        self.title.show()
        self.adjustSize()

    def setDetail(self, text):
        text=text.strip()
        self.detail.setText(text)
        self.detail.adjustSize()
        self.detail.show()
        self.adjustSize()

    def setInformation(self, text):
        text=text.strip()
        self.information.setText(text)
        self.information.adjustSize()
        self.information.show()
        self.adjustSize()

    def setTimer(self, timeout):
        QTimer.singleShot(timeout, self.hide)

    @key('p')
    def pauseAction(self, request={}):
        self.pause=True

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.pause=False
            self.hide()
        elif event.key()==Qt.Key_Space:
            self.pause=True

    @key('h')
    def hide(self):
        if not self.pause:
            super().hide()
            self.title.setText('')
            self.information.setText('')
            self.detail.setText('')
            self.messageHidden.emit()

    def hideAction(self, request):
        self.pause=False
        self.hide()
