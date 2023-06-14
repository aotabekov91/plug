#!/usr/bin/python4
import os
import inspect
from configparser import RawConfigParser

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .base import BaseQT

class Widget(BaseQT, QWidget):

    def __init__(self, name=None, config=None, leader=None, app=None):
        super(Widget, self).__init__(name, config, leader, argv=app)
        self.app=app
        self.setConfig()

    def toggle(self):
        if not self.activated:
            self.activate()
        else:
            self.deactivate()
    
    def activate(self, focus=True):
        if not self.activated:
            self.activated=True
            self.show()
            self.setFocus()

    def deactivate(self):
        if self.activated:
            self.activated=False
            self.hide()

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.deactivate()
        else:
            super().keyPressEvent(event)
