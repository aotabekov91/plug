import plug
from PyQt5 import QtCore 
from plug.qt import utils

class Plug(plug.Plug, QtCore.QObject):

    focusLost=QtCore.pyqtSignal(object)
    focusGained=QtCore.pyqtSignal(object)
    endedListening=QtCore.pyqtSignal(object)
    startedListening=QtCore.pyqtSignal(object)

    def setup(self):

        self.activated = False
        if self.isMainApp: 
            self.setupUIMan()
        super().setup()
        if self.isMainApp: 
            self.setEarMan()
        self.app.uiman.setupUIKeys(self)

    def setupUIMan(self):

        self.uiman=utils.UIMan()
        self.uiman.setApp(self)
        self.uiman.setAppUI(self)

    def setModer(self, moder=utils.Moder):
        super().setModer(moder)

    def setEarMan(self, earman=utils.EarMan):
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
        return self.octivate()

    def setFocus(self):

        c=self.app.earman.isListening(self)
        if not c: self.activate()
            
    def activate(self):

        self.activated=True
        self.app.uiman.activate(self)
        self.app.moder.modeWanted.emit(self)

    def octivate(self):

        self.activated=False
        self.app.uiman.octivate(self)
        self.app.moder.delistenWanted.emit()
