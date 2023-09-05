import os
import re
from PyQt5 import QtCore, QtWidgets

from plug import Plug as BasePlug
from plug.qt.utils import (ZMQListener, 
                           KeyListener, 
                           EventListener)

class Plug(BasePlug):

    respond=QtCore.pyqtSignal(dict)

    def __init__(self, app=None, **kwargs):

        self.app=app
        self.kwargs=kwargs
        self.command_activated=False

        super(Plug, self).__init__(**kwargs)

    def setup(self):

        super().setup()
        self.setEventListener(**self.kwargs)
        self.setActions()

    def setEventListener(self, **kwargs):

        self.event_listener=EventListener(
                obj=self, app=self.app, **kwargs)

    def setListener(self):

        self.listener = QtCore.QThread()
        self.zeromq_listener=ZMQListener(self)
        self.zeromq_listener.moveToThread(
                self.listener)
        self.listener.started.connect(
                self.zeromq_listener.loop)
        self.zeromq_listener.request.connect(
                self.act)
        QtCore.QTimer.singleShot(
                0, self.listener.start)

    def setSystemListener(self):

        self.os_thread = QtCore.QThread()
        self.os_listener=KeyListener(self)
        self.os_listener.moveToThread(self.os_thread)
        self.os_thread.started.connect(
                self.os_listener.loop)
        QtCore.QTimer.singleShot(0, self.os_thread.start)

    def act(self, request):

        response=self.handle(request)
        if self.respond_port:
            self.socket.send_json(response)
        self.zeromq_listener.acted=True

    def setConnection(self, kind='PULL'):

        super().setConnection(kind)
        if self.port or self.listen_port:
            self.setListener()

    def toggleCommandMode(self):

        if self.command_activated:
            self.deactivateCommandMode()
        else:
            self.activateCommandMode()

    def deactivateCommandMode(self):

        self.command_activated=False
        if self.ui.current==self.ui.commands: 
            self.ui.show(self.ui.previous)

    def activateCommandMode(self):

        self.command_activated=True
        self.ui.show(self.ui.commands)

    def listen(self): 

        self.event_listener.listen()
        if hasattr(self, 'ui') and self.activated: 
            self.ui.setFocus()

    def delisten(self): 

        self.event_listener.delisten()

    def checkLeader(self, event):

        return self.event_listener.checkLeader(
                event, kind='listen_leader')
