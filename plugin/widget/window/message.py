from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..message import MessageWidget
from .central import CentralWindow

class MessageWindow (CentralWindow):

    returnPressed=pyqtSignal()

    def __init__(self, app, window_title=''):
        super(MessageWindow, self).__init__(app, window_title)

        self.setGeometry(0, 0, 700, 100)

        self.message=MessageWidget()
        # self.message=QLabel('FUCK')
        # self.message.setStyleSheet('background-color: red;')
        self.message.hideWanted.connect(self.hideAction)
        self.setMainWidget(self.message)
        self.setCurrentWidget(self.message)

    def setTitle(self, text):
        self.message.setTitle(text)

    def setDetail(self, text):
        self.message.setDetail(text)

    def setInformation(self, text):
        self.message.setInformation(text)

    def setTimer(self, timeout):
        self.message.setTimer(timeout)

    def setPause(self):
        self.message.setPause()
