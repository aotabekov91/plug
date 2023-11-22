import plug
from PyQt5 import QtCore 
from plug.qt.utils import UIMan, EarMan, Moder

class Plug(plug.Plug, QtCore.QObject):

    focusLost=QtCore.pyqtSignal(object)
    focusGained=QtCore.pyqtSignal(object)
    endedListening=QtCore.pyqtSignal(object)
    startedListening=QtCore.pyqtSignal(object)

    def setup(self):

        self.activated = False
        if self.main_app: 
            self.setupUIMan()
        super().setup()
        if self.main_app: 
            self.setEarMan()
        self.app.uiman.setupUIKeys(self)

    def setupUIMan(self):

        self.uiman=UIMan()
        self.uiman.setApp(self)
        self.uiman.setAppUI(self)

    def setModer(self, moder=Moder):
        super().setModer(moder)

    def setEarMan(self, earman=EarMan):
        self.earman=earman(self)

    def listen(self): 

        self.startedListening.emit(self)
        self.app.earman.listen(self)
        self.app.uiman.focus(self)

    def delisten(self): 

        self.endedListening.emit(self)
        self.app.earman.delisten(self)
        self.app.uiman.defocus(self)

    def toggle(self):

        if not self.activated:
            return self.activate()
        return self.deactivate()

    def setFocus(self):

        c=self.app.earman.isListening(self)
        if not c: self.activate()
            
    def activate(self):

        self.activated=True
        self.app.uiman.activate(self)
        self.app.moder.modeWanted.emit(self)

    def deactivate(self):

        self.activated=False
        self.app.uiman.deactivate(self)
        self.app.moder.delistenWanted.emit()
