from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..browser import BrowserWidget 
from .central import CentralWindow

class BrowserWindow (CentralWindow):

    returnPressed=pyqtSignal()
    textChanged=pyqtSignal()

    def __init__(self, app, window_title='', label_title=''):
        super(BrowserWindow, self).__init__(app, window_title)

        self.setGeometry(0, 0, 700, 500)

        self.browser=BrowserWidget(label_title)

        self.browser.returnPressed.connect(self.returnPressed)
        self.browser.textChanged.connect(self.textChanged)

        self.setMainWidget(self.browser)
        self.setCurrentWidget(self.browser)

    def doneAction(self, *args, **kwargs):
        self.currentWidget().clear()
        self.hide()

    def setCSS(self, css):
        self.browser.setCSS(css)

    def setHTML(self, html):
        self.browser.setHTML(html)

    def text(self):
        return self.browser.text()

    def setText(self, text):
        self.browser.setText(text)

    def clear(self):
        self.browser.clear()

