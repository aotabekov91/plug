import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..list import ListWidget

class CentralWindow (QMainWindow):

    keysInputReturnPressed=pyqtSignal()
    keysListReturnPressed=pyqtSignal()

    def __init__ (self, app, window_title=''):
        super(CentralWindow, self).__init__()

        self.mode=app
        self.mode_listen=False
        self.current_widget=None
        self.main_widget=None

        self.socket=app.socket

        self.setWindowTitle(window_title)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.stack=QStackedWidget()
        self.setKeysHelper()
        self.setCentralWidget(self.stack)

    def setMainWidget(self, widget):
        widget.stack_id=self.stack.addWidget(widget)
        self.main_widget=widget

    def mainWidget(self):
        return self.main_widget

    def installEventFilter(self, listener):
        for i in range(self.stack.count()):
            self.stack.widget(i).installEventFilter(listener)

    def showMainWidget(self, request={}):
        self.show()
        self.stack.show()
        self.setCurrentWidget(self.main_widget)
        self.main_widget.setFocus()

    def addToStack(self, widget):
        widget.stack_id=self.stack.addWidget(widget)

    def setCurrentWidget(self, widget=None):
        if not widget: widget=self.main_widget
        self.stack.setCurrentIndex(widget.stack_id)
        self.current_widget=widget
        self.current_widget.show()
        self.current_widget.setFocus()

    def currentWidget(self):
        return self.current_widget

    def setKeysHelper(self):
        self.keys=ListWidget('Keys') 
        self.keys.inputReturnPressed.connect(self.keysInputReturnPressed)
        self.keys.listReturnPressed.connect(self.keysListReturnPressed)
        self.keys.stack_id=self.stack.addWidget(self.keys)

    def toggleKeysHelper(self):
        if self.keys.isVisible():
            self.setCurrentWidget(self.main_widget)
        else:
            dlist=[{'top':'No keys assigned'}]
            for func_name in self.mode.__dir__():
                func=getattr(self.mode, func_name)
                key=getattr(func, 'key', None)
                if key:
                    dlist+=[{'top': f'{key} {func_name}', 'id':func}]
            self.keys.setList(dlist)
            self.setCurrentWidget(self.keys)

    def showAction(self, *args, **kwargs):
        self.show()
        self.currentWidget().show()
        self.currentWidget().setFocus()

    def toggleShowAction(self, *args, **kwargs):
        if self.isVisible():
            self.hide()
        else:
            self.showAction()

    def doneAction(self, *args, **kwargs):
        self.hide()

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

    def hideAction(self, *args, **kwargs): 
        self.hide()

    def setFocus(self):
        self.currentWidget().setFocus()
