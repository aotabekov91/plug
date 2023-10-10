from PyQt5.QtCore import QObject, pyqtSignal

from plug.plugs.moder import Moder as Base

class Moder(Base, QObject):

    keysChanged=pyqtSignal(
            str)
    modeChanged=pyqtSignal(
            object)
    plugAdded=pyqtSignal(
            object)
    plugsLoaded=pyqtSignal(
            object)
    actionsRegistered=pyqtSignal(
            object, object)

    def add(self, plug):

        super().add(plug)
        if hasattr(plug, 'keysChanged'):
            plug.keysChanged.connect(
                    self.keysChanged)
        self.plugAdded.emit(plug)

    def load(self, *args, **kwargs):

        super().load(*args, **kwargs)
        self.plugsLoaded.emit(self.plugs)

    def set(self, mode=None):

        super().set(mode)
        self.modeChanged.emit(self.current)

    def save(self, plug, actions):

        super().save(plug, actions)
        self.actionsRegistered.emit(plug, actions)
