from PyQt5 import QtCore
from plug.utils import Plugman as Base

class Plugman(Base, QtCore.QObject):

    modeChanged=QtCore.pyqtSignal(object)

    def add(self, picked, kind):

        super().add(picked, kind)

        if hasattr(picked, 'modeWanted'):
            picked.modeWanted.connect(self.set)
        if hasattr(picked, 'forceDelisten'):
            picked.forceDelisten.connect(self.set)
        if hasattr(picked, 'delistenWanted'):
            picked.delistenWanted.connect(self.set)


    def set(self, listener='normal', kind='mode'):

        super().set(listener, kind)
        self.modeChanged.emit(self.current)



