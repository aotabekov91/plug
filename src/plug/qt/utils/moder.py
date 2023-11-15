from plug import utils
from PyQt5.QtCore import QObject, pyqtSignal

class Moder(utils.Moder, QObject):

    delistenWanted=pyqtSignal()
    plugAdded=pyqtSignal(object)
    modeWanted=pyqtSignal(object)
    modeChanged=pyqtSignal(object)
    plugsLoaded=pyqtSignal(object)
    modeIsToBeSet=pyqtSignal(object)
    actionsRegistered=pyqtSignal(object, object)

    def setup(self):

        super().setup()
        self.modeWanted.connect(
                self.set)
        self.delistenWanted.connect(
                self.set)
        self.app.uiman.appLaunched.connect(
                self.setupOnLauch)

    def setupOnLauch(self):

        self.set(self.default)
        w=getattr(self.app, 'window', None)
        if w: w.focusGained.connect(self.reset)

    def reset(self):
        self.set(self.current)

    def add(self, plug):

        super().add(plug)
        self.plugAdded.emit(plug)

    def load(self, *args, **kwargs):

        super().load(*args, **kwargs)
        self.plugsLoaded.emit(self.plugs)

    def set(self, mode=None):

        m=self.get(mode)
        self.modeIsToBeSet.emit(m)
        m=super().set(m)
        if m: self.modeChanged.emit(m)
        return m

    def save(self, plug, actions):

        super().save(plug, actions)
        self.actionsRegistered.emit(plug, actions)
