from plug.plugs.moder import Moder as Base
from PyQt5.QtCore import QObject, pyqtSignal

class Moder(Base, QObject):

    keysChanged=pyqtSignal(
            str)
    modeIsToBeSet=pyqtSignal(
            object)
    modeChanged=pyqtSignal(
            object)
    detailChanged=pyqtSignal(
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

        mode=self.get(mode)
        self.modeIsToBeSet.emit(mode)
        m=super().set(mode)
        if m: self.modeChanged.emit(m)
        return m

    def save(self, plug, actions):

        super().save(plug, actions)
        self.actionsRegistered.emit(
                plug, actions)
