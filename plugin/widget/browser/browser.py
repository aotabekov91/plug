import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from ..input import InputWidget
from .qbrowser import Browser

class BrowserWidget (QWidget):

    textChanged=pyqtSignal()
    returnPressed=pyqtSignal()

    def __init__ (self, label_title=''):
        super(BrowserWidget, self).__init__()

        self.waiting=False
        self.setGeometry(0, 0, 700, 100)
        self.setFixedSize(QSize(700, 500))

        self.style_sheet='''
            QWidget{
                font-size: 16px;
                color: black;
                background-color: transparent; 
                border-width: 0px;
                border-radius: 0px;
                }
            QWidget#browserContainer{
                border-color: red;
                border-width: 2px;
                border-radius: 10px;
                border-style: outset;
                background-color: white;
                }
                '''

        self.input=InputWidget()
        self.input.setLabel(label_title)
        self.input.setMaximumHeight(58)

        self.browser = Browser()

        w=QWidget(objectName='browserContainer')
        layout=QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(7,7,7,7)
        layout.addWidget(self.browser)
        w.setLayout(layout)
        w.setStyleSheet(self.style_sheet)


        layout=QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(self.input)
        layout.addWidget(w)

        self.setLayout(layout)

        self.setStyleSheet(self.style_sheet)

        self.input.textChanged.connect(self.textChanged)
        self.input.returnPressed.connect(self.returnPressed)

    def installEventFilter(self, listener):
        self.input.installEventFilter(listener)
        self.browser.installEventFilter(listener)

    def showAction(self, request):
        self.browser.show()
        self.input.setFocus()

    def setFocus(self):
        self.input.setFocus()

    def setCSS(self, css):
        self.browser.loadCSS(css)

    def setHTML(self, html):
        self.browser.loadHtml(html)

    def text(self):
        return self.input.text()

    def setText(self, text):
        self.input.setText(text)

    def clear(self):
        self.input.clear()
