from PyQt5 import QtCore 
from plug import Plug as Base
from plug.qt.utils import UIMan
from gizmo.utils import Ear, register

class Plug(Base, QtCore.QObject):

    position=None
    main_app=None

    appLaunched=QtCore.pyqtSignal()
    tabPressed=QtCore.pyqtSignal()
    escapePressed=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    carriagePressed=QtCore.pyqtSignal()
    delistenWanted=QtCore.pyqtSignal()
    focusLost=QtCore.pyqtSignal(object)
    focusGained=QtCore.pyqtSignal(object)
    modeWanted=QtCore.pyqtSignal(object)
    listenWanted=QtCore.pyqtSignal(object)
    keysChanged=QtCore.pyqtSignal(str)
    endedListening=QtCore.pyqtSignal(object)
    startedListening=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            *args, 
            wait=100,
            **kwargs
            ):

        self.wait=wait
        self.running = False
        self.activated = False
        super(Plug, self).__init__(
                *args, **kwargs)
        self.initiate()

    def initiate(self):

        if not self.app:
            self.uiman.setUIKeys()
        else:
            self.app.uiman.setUIKeys(obj=self)

    def setup(self):

        super().setup()
        if self.main_app:
            self.setUIMan()
        self.setTimer()
        self.setEar()
        if self.app:
            self.app.moder.add(self)

    def setUIMan(self):

        raise
        self.uiman=UIMan(
                obj=self, 
                **self.kwargs)
        self.uiman.setApp()
        self.uiman.setAppUI()

    def setTimer(self):

        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(
                self.launch)

    def setEar(self):

        self.ear=Ear(
                obj=self, **self.kwargs)

    def listen(self): 

        self.ear.listen()
        self.startedListening.emit(self)
        if not self.app:
            self.uiman.listen()
        else:
            self.app.uiman.listen(self)

    def delisten(self): 

        self.ear.delisten()
        self.endedListening.emit(self)
        if not self.app:
            self.app.uiman.delisten()
        else:
            self.app.uiman.delisten(self)

    def checkLeader(self, e, p=None): 
        return p in self.ear.listen_leader

    @register('t', modes=['command'])
    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    @register('f', modes=['command'])
    def setFocus(self):

        if not self.ear.listening:
            self.activate()
            
    def activate(self):

        self.activated=True
        self.modeWanted.emit(self)
        if not self.app:
            self.uiman.activate()
        else:
            self.app.uiman.activate(self)

    def deactivate(self):

        self.activated=False
        if self.ear.listening:
            self.delistenWanted.emit()
        if not self.app:
            self.uiman.deactivate()
        else:
            self.app.uiman.deactivate(self)

    def launch(self):

        self.timer.stop()
        self.appLaunched.emit()

    def run(self):

        self.running=True
        self.timer.start(self.wait)
        if not self.app:
            self.uiman.activate()
        else:
            self.uiman.activate(self)

    def exit(self): 

        self.running=False
        if not self.app:
            self.uiman.deactivate()
        else:
            self.uiman.deactivate(self)

    def getView(self):
        return None
