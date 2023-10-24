from PyQt5 import QtCore 
from plug import Plug as Base
from plug.qt.utils import UIMan
from gizmo.utils import Ear, register

class Plug(Base, QtCore.QObject):

    tabPressed=QtCore.pyqtSignal()
    escapePressed=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    forceDelisten=QtCore.pyqtSignal()
    carriagePressed=QtCore.pyqtSignal()
    delistenWanted=QtCore.pyqtSignal()
    focusLost=QtCore.pyqtSignal(
            object)
    focusGained=QtCore.pyqtSignal(
            object)
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
            self, 
            *args, 
            follow_focus=True,
            **kwargs):

        self.running = False
        self.activated = False
        self.follow_focus=follow_focus
        self.position=kwargs.get(
                'position', None)
        self.follow_mouse=kwargs.get(
                'follow_mouse', False)
        super(Plug, self).__init__(
                *args, **kwargs)

    def initiate(self):

        self.uiman.setUIKeys()
        super().initiate()

    def setup(self):

        super().setup()
        self.setUIMan()
        self.setEar()
        if self.app:
            self.app.moder.add(self)

    def setUIMan(self):

        self.uiman=UIMan(
                self, **self.kwargs)

    def setEar(self):

        self.ear=Ear(
                obj=self, **self.kwargs)

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

    @register('t', modes=['command'])
    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    @register('f', modes=['command'])
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
