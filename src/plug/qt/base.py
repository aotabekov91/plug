import os
import re
import threading
from PyQt5 import QtCore, QtWidgets

from plug import Plug as BasePlug

from .utils import ZMQListener, KeyListener, EventListener

class Plug(BasePlug):

    respond=QtCore.pyqtSignal(dict)

    def __init__(self, 
                 app=None, 
                 mode_keys={},
                 listen_leader=None,
                 command_leader='Ctrl+.',
                 **kwargs,
                 ):

        self.css={}
        self.app=app
        self.css_style=''
        self.mode_keys=mode_keys
        self.command_activated=False

        self.listen_leader=listen_leader
        self.command_leader=command_leader

        super(Plug, self).__init__(**kwargs)

        self.setShortcuts()
        self.setEventListener()

    def setCustomStyleSheet(self):

        if self.css_style:

            if self.app and self.app.css_style:
                style_sheet=self.css_style+self.app.css_style
            else:
                style_sheet=self.css_style

            if hasattr(self, 'setStyleSheet'):
                style_sheet=self.styleSheet()+style_sheet
                self.setStyleSheet(style_sheet)
            elif hasattr(self, 'ui'):
                style_sheet=self.ui.styleSheet()+style_sheet
                self.ui.setStyleSheet(style_sheet)

    def setFiles(self):

        super().setFiles()
        for f in os.listdir(self.path):

            if f.endswith('css'):
                path=f'{self.path}/{f}'
                with open(path, 'r') as y:
                    lines=' '.join(y.readlines())
                    lines=re.sub(r'[\n\t]', ' ', lines)
                    if f=='style.css':
                        self.css_style=lines
                    else:
                        self.css[path]=lines

    def setEventListener(self):

        self.event_listener=EventListener(
                obj=self,
                app=self.app)

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

    def setShortcuts(self):

        if self.config.get('Shortcuts'):
            shortcuts=self.config['Shortcuts']
            for name, key in shortcuts.items():
                func=getattr(self, name, None)
                if func:
                    shortcut=QtWidgets.QShortcut(key)
                    shortcut.activated.connect(func)
                    self.action[(key, name)]=func

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
