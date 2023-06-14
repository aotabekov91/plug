import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainWindow (QMainWindow):
    def __init__ (self, app, window_title=''):
        super(MainWindow, self).__init__()

        self.mode=app
        self.mode_listen=False
        self.socket=app.socket

        self.setWindowTitle(window_title)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def showAction(self, *args, **kwargs):
        self.show()
        self.setFocus()

    def toggleShowAction(self, *args, **kwargs):
        if self.isVisible():
            self.hide()
        else:
            self.showAction()

    def hideAction(self, *args, **kwargs):
        self.hide()

    def doneAction(self, *args, **kwargs):
        self.hide()

    def installEventFilter(self, listener):
        super().installEventFilter(listener)

