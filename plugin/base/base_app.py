import os
import sys
import zmq
import time
import inspect

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from os.path import abspath
from configparser import ConfigParser

from .base import BasePlugin
from .helper import ZMQListener 

class AppPlugin(BasePlugin, QApplication):
    def __init__(self, name=None, config=None, leader=None, port=None, app_name=None):

        self.port=port
        self.app_name=app_name
        super(AppPlugin, self).__init__(name, config, leader, argv=[])

        self.setAppName()
        self.setConnection()

    def setAppName(self):
        if not self.app_name: self.app_name=self.name
        self.setApplicationName(self.app_name)

    def setSettings(self):
        super().setSettings()
        if self.config.has_section('Settings'):
            if self.config.has_option('Settings', 'port') and not self.port:
                self.port=self.config.getint('Settings', 'port')

    def setConnection(self, exit=True):
        try:
            self.socket = zmq.Context().socket(zmq.PULL)
            if self.port:
                self.socket.bind(f'tcp://*:{self.port}')
            else:
                self.port=self.socket.bind_to_random_port('tcp://*')
            self.setListener()
        except:
            if self.port:
                socket = zmq.Context().socket(zmq.PUSH)
                socket.connect(f'tcp://localhost:{self.port}')
                socket.send_json({'command':'showAction'})
                if exit:
                    sys.exit()
                else:
                    return socket

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

    def setListener(self):
        self.listener = QThread()
        self.zeromq_listener=ZMQListener(self)
        self.zeromq_listener.moveToThread(self.listener)
        self.listener.started.connect(self.zeromq_listener.loop)
        self.zeromq_listener.request.connect(self.handleRequest)
        QTimer.singleShot(0, self.listener.start)

    def run(self):
        self.activated=True
        sys.exit(self.exec_())

    def exit(self, request={}):
        self.activated=False
        self.close()
        sys.exit()

if __name__=='__main__':
    app=AppPlugin(port=33333)
    app.run()
