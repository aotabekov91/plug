import plug
from PyQt5 import QtCore 
from gizmo.utils import Ear, register
from plug.qt.utils import UIMan, Moder

class Plug(plug.Plug, QtCore.QObject):

    position=None

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
        self.app.uiman.setUIKeys(self)

    def setup(self):

        super().setup()
        if self.main_app:
            self.setUIMan()
        self.setTimer()
        self.setEar()

    def setUIMan(self):

        self.uiman=UIMan()
        self.uiman.setApp(self)
        self.uiman.setAppUI(self)

    def setModer(self, moder=Moder):
        super().setModer(moder)

    def setTimer(self):

        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(
                self.launch)

    def setEar(self):

        self.ear=Ear(
                obj=self, 
                app=self.app,
                config=self.config,
                **self.kwargs
                )

    def listen(self): 

        self.ear.listen()
        self.startedListening.emit(self)
        self.app.uiman.listen(self)

    def delisten(self): 

        self.ear.delisten()
        self.endedListening.emit(self)
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
        self.app.uiman.activate(self)

    def deactivate(self):

        self.activated=False
        if self.ear.listening:
            self.delistenWanted.emit()
        self.app.uiman.deactivate(self)

    def launch(self):

        self.timer.stop()
        self.appLaunched.emit()

    def run(self):

        self.running=True
        self.timer.start(self.wait)
        self.app.uiman.activate(self)

    def exit(self): 

        self.running=False
        self.app.uiman.deactivate(self)

    def getView(self):
        return None
