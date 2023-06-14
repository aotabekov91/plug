from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainStackBase (QMainWindow):

    def __init__ (self, stack_class, window_title=''):
        super(MainStackBase, self).__init__()

        self.setWindowTitle(window_title)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.stack=stack_class()
        self.setCentralWidget(self.stack)

    def setMainWidget(self, widget):
        self.stack.setMainWidget(widget)

    def mainWidget(self):
        return self.stack.mainWidget()

    def installEventFilter(self, listener):
        self.stack.installEventFilter(listener)

    def showMainWidget(self, request={}):
        self.stack.showMainWidget()

    def addWidget(self, widget):
        return self.addWidget(widget)

    def currentWidget(self):
        return self.stack.currentWidget()

    def setFocus(self):
        self.stack.setFocus()

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Q, Qt.Key_Escape]:
            self.hide()
        elif event.modifiers():
            if event.key() in [Qt.Key_BracketLeft]:
                self.hide()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)
