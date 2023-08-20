import os
import re
import threading
from PyQt5 import QtCore, QtWidgets

from plug import Plug as BasePlug

from .utils import ZMQListener, KeyListener

class Plug(BasePlug):

    respond=QtCore.pyqtSignal(dict)

    def __init__(self, 
                 app=None, 
                 mode_keys={},
                 listen_leader=None,
                 command_leader='Ctrl+.',
                 **kwargs,
                 ):

        self.app=app
        self.css={}
        self.css_style=''
        self.mode_keys=mode_keys
        self.command_activated=False

        self.listen_modifiers=[]
        self.command_modifiers=[]
        self.listen_leader=listen_leader
        self.command_leader=command_leader

        super(Plug, self).__init__(**kwargs)

        self.setShortcuts()
        self.setLeaders()

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

    def modeKey(self, mode): 
        return self.mode_keys.get(mode, '')

    def setListener(self):

        self.listener = QtCore.QThread()
        self.zeromq_listener=ZMQListener(self)
        self.zeromq_listener.moveToThread(self.listener)
        self.listener.started.connect(
                self.zeromq_listener.loop)
        self.zeromq_listener.request.connect(self.act)
        QtCore.QTimer.singleShot(0, self.listener.start)

    def act(self, request):

        response=self.handle(request)
        if self.respond_port:
            self.socket.send_json(response)
        self.zeromq_listener.acted=True

    def setOSListener(self):

        self.os_thread = QtCore.QThread()
        self.os_listener=KeyListener(self)
        self.os_listener.moveToThread(self.os_thread)
        self.os_thread.started.connect(
                self.os_listener.loop)
        QtCore.QTimer.singleShot(0, self.os_thread.start)

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

    def eventFilter(self, widget, event):

        if event.type()==QtCore.QEvent.KeyPress:

            if self.command_leader:
                c=hasattr(self, 'ui') 
                c=c and hasattr(self.ui, 'commands')
                if c:
                    c1=self.checkKey(event, 'command_leader')
                    if c1:
                        if self.command_activated:
                            self.deactivateCommandMode()
                        else:
                            self.activateCommandMode()
                        event.accept()
                        return True

        return super().eventFilter(widget, event)

    def setLeaders(self):

        def _set(leader):

            mapping={',': 'Comma',
                     ';': 'Semicolon', 
                     '.': 'Period'}

            modifiers, key_values = [], []

            if leader:
                set_key=leader.split('+')
                for i, k in enumerate(set_key):
                    if k in ['Ctrl', 'Alt', 'Shift']:
                        modifiers+=[k]
                    else:
                        break

                if modifiers:
                    for k in set_key[i:]:
                        k=mapping.get(k, k.upper())
                        v=getattr(QtCore.Qt, f"Key_{k}", k)
                        key_values+=[v]
                else:
                    key_values=set_key[i:]

            return modifiers, key_values

        def set():

            lmode, lval=_set(self.listen_leader)
            cmode, cval=_set(self.command_leader)

            self.listen_leader=lval
            self.listen_modifiers=lmode

            self.command_leader=cval
            self.command_modifiers=cmode

        t=threading.Thread(target=set)
        t.start()

    def checkKey(self, event, kind='listen_leader'):

        mod=[]
        mdf=event.modifiers()
        if mdf==QtCore.Qt.AltModifier:
            mod+=['Alt']
        if mdf==QtCore.Qt.ControlModifier:
            mod+=['Ctrl']
        if mdf==QtCore.Qt.ShiftModifier:
            mod+=['Shift']

        if kind=='listen_leader':

            cval=self.listen_leader
            cmode=self.listen_modifiers

        elif kind=='command_leader':

            cval=self.command_leader
            cmode=self.command_modifiers

        if mod==cmode:
            if cmode:
                return cval==[event.key()]
            else:
                return cval==[event.text()]
        return False

    def deactivateCommandMode(self):

        self.command_activated=False
        if self.ui.current==self.ui.commands: 
            self.ui.show(self.ui.previous)

    def activateCommandMode(self):

        self.command_activated=True
        self.ui.show(self.ui.commands)
