from plug import utils
from PyQt5.QtCore import QObject, pyqtSignal

class Moder(utils.Moder, QObject):

    delistenWanted=pyqtSignal()
    plugAdded=pyqtSignal(object)
    modeAdded=pyqtSignal(object)
    modeWanted=pyqtSignal(object)
    modeChanged=pyqtSignal(object)
    plugsLoaded=pyqtSignal(object)
    modeIsToBeSet=pyqtSignal(object)
    actionsRegistered=pyqtSignal(object, object)

    def setup(self):

        super().setup()
        self.modeWanted.connect(
                self.setMode)
        self.delistenWanted.connect(
                self.setMode)
        self.app.uiman.appLaunched.connect(
                self.launch)

    def launch(self):

        self.setMode(self.default)
        w=getattr(self.app, 'window', None)
        if w: w.focusGained.connect(self.reset)

    def reset(self):
        self.setMode(self.current)

    def add(self, p):

        super().add(p)
        self.plugAdded.emit(p)
        if p.isMode: 
            self.modeAdded.emit(p)

    def load(self, *args, **kwargs):

        super().load(*args, **kwargs)
        self.plugsLoaded.emit(self.plugs)

    def setMode(self, mode=None):

        m=self.getMode(mode)
        self.modeIsToBeSet.emit(m)
        m=super().setMode(m)
        if m: self.modeChanged.emit(m)
        return m

    def save(self, plug, actions):

        super().save(plug, actions)
        self.actionsRegistered.emit(plug, actions)
