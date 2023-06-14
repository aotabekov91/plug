import os
import sys
import zmq
import time
import inspect

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from os.path import abspath
from configparser import RawConfigParser

class BasePlugin:

    def __init__(self, name=None, config=None, leader=None, argv=None):
        if argv!=None:
            super(BasePlugin, self).__init__(argv)
        else:
            super(BasePlugin, self).__init__()

        self.name=name
        self.leader=leader
        self.config=config

        self.activated = False
        self.leader_activated=False

        self.setName()
        self.setLeader()
        self.setConfig()
        self.setShortcuts()
        self.setSettings()

    def readConfig(self): 
        file_path=os.path.abspath(inspect.getfile(self.__class__))
        mode_path=os.path.dirname(file_path).replace('\\', '/')
        config_path=f'{mode_path}/config.ini'
        config=RawConfigParser()
        config.optionxform=str
        config.read(config_path)
        return config

    def setLeader(self):
        if self.leader is None: 
            self.leader='.'

    def setName(self):
        if self.name is None: 
            self.name=self.__class__.__name__

    def setConfig(self):
        if self.config is None:
            self.config=self.readConfig()

    def setSettings(self):
        if self.config.has_section('Settings'):
            config=dict(self.config['Settings'])
            for name, value in config.items():
                func=setattr(self, name, value)

    def setShortcuts(self):
        if self.config.has_section('Shortcuts'):
            config=dict(self.config['Shortcuts'])
            for func_name, key in config.items():
                func=getattr(self, func_name, None)
                if func:
                    shortcut=QShortcut(key)
                    shortcut.activated.connect(func)
                    self.actions[f'{self.name}_{func_name}']=func

    def action(self, event):
        for func_name in self.__dir__():
            func=getattr(self, func_name)
            if not hasattr(func, 'key'): continue
            if event.text()==func.key or event.key()==func.key:
                func()
                event.accept()
                return 
        return event

    def eventFilter(self, widget, event):
        if event.type()==QEvent.KeyPress:
            if self.leader_activated:
                self.leader_activated=False
                event=self.action(event)
                if not event:
                    return True
                else:
                    return widget.event(event)
            elif event.text()==self.leader:
                self.leader_activated=True
                return True
            else:
                return widget.event(event)
        else:
            return widget.event(event)
