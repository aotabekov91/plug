from PyQt5 import QtCore 
from gizmo.utils import Ear
from plug import Plug as Base
from plug.qt.utils import UIMan

class Plug(Base, QtCore.QObject):

    escapePressed=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    forceDelisten=QtCore.pyqtSignal()
    delistenWanted=QtCore.pyqtSignal()
    modeWanted=QtCore.pyqtSignal(
            object)
    listenWanted=QtCore.pyqtSignal(
            object)
    keysChanged=QtCore.pyqtSignal(
            str)
    keyPressed=QtCore.pyqtSignal(
            object, object)
    endedListening=QtCore.pyqtSignal(
            object)
    startedListening=QtCore.pyqtSignal(
            object)

    def __init__(
            self, *args, **kwargs):

        self.running = False
        self.activated = False
        self.position=kwargs.get(
                'position', None)
        self.follow_mouse=kwargs.get(
                'follow_mouse', False)
        super(Plug, self).__init__(
                *args, **kwargs)

    def initialize(self):

        self.uiman.setUIKeys()
        super().initiate()

    def setup(self):

        super().setup()
        self.setUIMan()
        self.setEar()
        if self.app:
            self.app.moder.add(self)

    def getUpdatedArgs(self):

        kwargs=self.kwargs.copy()
        settings=self.config.get('Settings', {})
        kwargs.update(settings)
        return kwargs

    def setUIMan(self):

        self.uiman=UIMan(
                self,
                **self.getUpdatedArgs(),
                )

    def setEar(self):

        self.ear=Ear(
                obj=self, 
                **self.getUpdatedArgs(),
                )

    def listen(self): 

        self.ear.listen()
        self.uiman.listen()
        self.startedListening.emit(self)

    def delisten(self): 

        self.ear.delisten()
        self.uiman.delisten()
        self.endedListening.emit(self)

    def checkLeader(self, e, p=None): 

        return p in self.ear.listen_leader

    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    def setMode(self, mode):

        if self.app:
            mode=self.app.moder.get(mode)
            if mode: mode.activate()
        
    def activate(self):

        self.activated=True
        self.uiman.activate()
        self.modeWanted.emit(self)

    def deactivate(self):

        self.activated=False
        self.uiman.deactivate()
        if self.ear.listening:
            self.delistenWanted.emit()

    def run(self):

        self.running=True
        self.uiman.activate()

    def exit(self): 

        self.running=False
        self.uiman.deactivate()
