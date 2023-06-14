import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .base import BaseQT

class App(BaseQT, QApplication):
    def __init__(self, name=None, config=None, leader=None, port=None, app_name=None):
        super(App, self).__init__(name, config, leader, port) 
        self.app_name=app_name
        self.setAppName()

    def setAppName(self):
        if not self.app_name: self.app_name=self.name
        self.setApplicationName(self.app_name)

    def handleRequest(self, request):
        command=request['command']

        mode_func=getattr(self, command, None)

        ui_func=None
        if hasattr(self, 'ui'):
            ui_func=getattr(self.ui, command, None)

        if mode_func:
            mode_func(request)
            msg=f"{self.__class__.__name__}: handled request"
        elif ui_func:
            ui_func(request)
            msg=f"{self.__class__.__name__}: UI handled request"
        else:
            msg=f'{self.__class__.__name__}: not understood'

        print(msg)

    def run(self):
        self.running=True
        self.setListener()
        sys.exit(self.exec_())

    def exit(self, request={}):
        self.running=False
        self.close()
        sys.exit()

if __name__=='__main__':
    app=App(port=33333)
    app.run()
