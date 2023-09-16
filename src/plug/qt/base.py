from PyQt5 import QtCore

from plug import Plug as BasePlug
from plug.qt.utils import EventListener

class Plug(BasePlug, QtCore.QObject):

    endedListening=QtCore.pyqtSignal(object)
    startedListening=QtCore.pyqtSignal(object)

    forceDelisten=QtCore.pyqtSignal()
    delistenWanted=QtCore.pyqtSignal()
    modeWanted=QtCore.pyqtSignal(object)
    listenWanted=QtCore.pyqtSignal(object)
    escapePressed=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    keysChanged=QtCore.pyqtSignal(str)
    keyPressed=QtCore.pyqtSignal(object, object)

    def __init__(self, app=None, **kwargs):

        self.app=app
        self.listening=False
        self.command_activated=False
        super(QtCore.QObject).__init__()
        super(BasePlug, self).__init__(**kwargs)

    def setup(self):

        super().setup()
        self.setEventListener(**self.kwargs)
        self.setActions()

    def setEventListener(self, **kwargs):

        self.event_listener=EventListener(
                obj=self, app=self.app, **kwargs)

    def toggleCommandMode(self):

        if self.command_activated:
            self.deactivateCommandMode()
        else:
            self.activateCommandMode()

    def deactivateCommandMode(self):

        if hasattr(self, 'ui'):
            self.command_activated=False
            if self.ui.current==self.ui.commands: 
                self.ui.show(self.ui.previous)

    def activateCommandMode(self):

        if hasattr(self, 'ui'):
            self.command_activated=True
            self.ui.show(self.ui.commands)

    def listen(self): 

        self.listening=True
        self.event_listener.listen()
        if hasattr(self, 'ui') and self.activated: 
            self.ui.setFocus()
        self.startedListening.emit(self)

    def delisten(self): 

        self.listening=False
        self.event_listener.delisten()
        self.endedListening.emit(self)

    def checkLeader(self, event, pressed=None): 

        l=self.event_listener.listen_leader
        return pressed in l
