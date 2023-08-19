from PyQt5 import QtCore

from plug.qt.utils import register as reg
from plug.utils import Plugman as Base

class Plugman(Base, QtCore.QObject):

    keysChanged=QtCore.pyqtSignal(str)
    modeChanged=QtCore.pyqtSignal(object)

    def setup(self):

        super().setup()
        funcs=['installPicks', 'updatePicks', 'cleanupPicks']
        actions={}
        for f in funcs:
            d=(self.__class__.__name__, f)
            m=getattr(self, f)
            func=lambda *args, **kwargs: m(*args, **kwargs)
            func.name=f
            func.modes=['exec']
            actions[d]=func
        self.register(self, actions)

    def installPicks(self): super().installPicks()

    def updatePicks(self): super().updatePicks()

    def cleanupPicks(self): super().cleanupPicks()

    def add(self, picked, kind):

        super().add(picked, kind)

        if hasattr(picked, 'modeWanted'):
            picked.modeWanted.connect(self.set)
        if hasattr(picked, 'forceDelisten'):
            picked.forceDelisten.connect(self.set)
        if hasattr(picked, 'delistenWanted'):
            picked.delistenWanted.connect(self.set)
        if hasattr(picked, 'keysChanged'):
            picked.keysChanged.connect(self.keysChanged)

    def set(self, listener='normal', kind='mode'):

        super().set(listener, kind)
        self.modeChanged.emit(self.current)
