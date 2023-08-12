from PyQt5 import QtCore, QtWidgets

from plug import Plug as BasePlug

from ..utils import ZMQListener, KeyListener

class Plug(BasePlug):

    respond=QtCore.pyqtSignal(dict)

    def __init__(self, 
                 app=None, 
                 mode_keys={},
                 command_leader='Ctrl+.',
                 **kwargs,
                 ):

        self.app=app
        self.mode_keys=mode_keys
        self.command_activated=False
        self.command_leader=command_leader

        super(Plug, self).__init__(**kwargs)

        self.setShortcuts()

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

        if self.config.has_section('Shortcuts'):
            config=dict(self.config['Shortcuts'])
            for func_name, key in config.items():
                func=getattr(self, func_name, None)
                if func:
                    shortcut=QtWidgets.QShortcut(key)
                    shortcut.activated.connect(func)
                    self.action[(key, func_name)]=func

    def eventFilter(self, widget, event):

        if event.type()==QtCore.QEvent.KeyPress:

            if self.command_leader:
                c=hasattr(self, 'ui') 
                c=c and hasattr(self.ui, 'commands')
                if c:
                    c1=self.checkKey(event, self.command_leader)
                    if c1:
                        if self.command_activated:
                            self.deactivateCommandMode()
                        else:
                            self.activateCommandMode()
                        event.accept()
                        return True

        return super().eventFilter(widget, event)

    def setKey(self, set_key):

        if set_key:
            set_key=set_key.split('+')
            set_key=sorted(set_key[:-1])+set_key[-1:]
            return '+'.join(set_key)

    def checkKey(self, event, check_key):

        if check_key:
            key=event.text()
            if check_key[-1]==key:
                mod=[]
                if len(check_key)==1:
                    return True
                else:
                    mdf=event.modifiers()
                    if mdf==QtCore.Qt.AltModifier:
                        mod+=['Alt']
                    if mdf==QtCore.Qt.ControlModifier:
                        mod+=['Ctrl']
                    if mdf==QtCore.Qt.ShiftModifier:
                        mod+=['Shift']
                    pressed='+'.join(mod+[key])
                    if check_key==pressed: 
                        return True

    def deactivateCommandMode(self):

        self.command_activated=False
        if self.ui.current==self.ui.commands: 
            self.ui.show(self.ui.previous)

    def activateCommandMode(self):

        self.command_activated=True
        self.ui.show(self.ui.commands)
