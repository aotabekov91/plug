import os
import sys
import zmq
import time

import threading

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ..base import Base
from .helper import ZMQListener 

class BaseQT(Base):

    fileCreated=pyqtSignal(str)

    def __init__(self, name=None, config=None, leader=None, port=None, argv=[]):
        super(BaseQT, self).__init__(name, config, port, argv)

        self.leader=[]
        self.setLeader(leader)
        self.leader_activated=False

    def setLeader(self, leader):
        self.leader=leader
        if self.leader is None: 
            self.leader=['.']
        if type(self.leader)==str:
            self.leader=[self.leader]

    def addLeader(self, leader):
        if not leader in self.leader:
            self.leader+=[leader]

    def setListener(self):
        self.listener = QThread()
        self.zeromq_listener=ZMQListener(self)
        self.zeromq_listener.moveToThread(self.listener)
        self.listener.started.connect(self.zeromq_listener.loop)
        self.zeromq_listener.request.connect(self.handleRequest)
        QTimer.singleShot(0, self.listener.start)

    def setConnection(self, exit=True, kind=zmq.PULL):
        try:
            self.socket = zmq.Context().socket(kind)
            if self.port:
                self.socket.bind(f'tcp://*:{self.port}')
            else:
                self.port=self.socket.bind_to_random_port('tcp://*')
        except:
            if self.port:
                socket = zmq.Context().socket(zmq.PUSH)
                socket.connect(f'tcp://localhost:{self.port}')
                socket.send_json({'command':'showAction'})
                if exit:
                    sys.exit()
                else:
                    return socket

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
            if getattr(func, 'leader', None) and self.leader_pressed!=func.leader: continue
            if event.text()==func.key or event.key()==func.key:
                func()
                event.accept()
                return 
        return event

    def watchFile(self, fList):
        def watch(file, timeout=300):
            i=0
            if not os.path.exists(file):
                while i<timeout:
                    i+=1
                    time.sleep(1)
                    if os.path.exists(file):
                        self.fileCreated.emit(file)
                        return
        if type(fList)!=list: fList=[fList]
        for file in fList:
            if file:
                t=threading.Thread(target=watch, args=(file,))
                t.deamon=True
                t.start()

    def eventFilter(self, widget, event):
        if event.type()==QEvent.KeyPress:
            if self.leader_activated:
                self.leader_activated=False
                event=self.action(event)
                if not event:
                    return True
                else:
                    return widget.event(event)
            elif event.text() in self.leader:
                self.leader_activated=True
                self.leader_pressed=event.text()
                return True
            else:
                return widget.event(event)
        else:
            return widget.event(event)
