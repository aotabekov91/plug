from PyQt5.QtCore import QObject, pyqtSignal

from gizmo.utils import register
from plug.utils import Moder as Base
from plug.qt.utils.picky import Picky

class Moder(Base, QObject):

    keysChanged=pyqtSignal(str)
    modeChanged=pyqtSignal(object)
    plugAdded=pyqtSignal(object)
    plugsLoaded=pyqtSignal(object)
    actionsRegistered=pyqtSignal(
            object, object)

    def setPicky(self, picky_class=None):
        super().setPicky(picky_class=Picky)

    def add(self, plug):

        super().add(plug)
        if hasattr(plug, 'modeWanted'):
            plug.modeWanted.connect(
                    self.set)
        if hasattr(plug, 'forceDelisten'):
            plug.forceDelisten.connect(
                    self.set)
        if hasattr(plug, 'delistenWanted'):
            plug.delistenWanted.connect(
                    self.set)
        if hasattr(plug, 'keysChanged'):
            plug.keysChanged.connect(
                    self.keysChanged)
        self.plugAdded.emit(plug)

    def load(self, plugs=set()):

        super().load(plugs)
        self.plugsLoaded.emit(self.plugs)

    def set(self, mode=None):

        super().set(mode)
        self.modeChanged.emit(self.current)

    def save(self, plug, actions):

        super().save(plug, actions)
        self.actionsRegistered.emit(plug, actions)
