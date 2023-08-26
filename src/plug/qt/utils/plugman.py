from PyQt5 import QtCore

from plug.utils import Plugman as Base
from plug.qt.utils.register import register

class Plugman(Base, QtCore.QObject):

    keysChanged=QtCore.pyqtSignal(str)
    modeChanged=QtCore.pyqtSignal(object)
    actionsRegistered=QtCore.pyqtSignal()

    def setup(self):

        super().setup()
        funcs=['installPicks', 
               'updatePicks', 
               'cleanupPicks']
        actions={}
        for f in funcs:
            actions[('Plugman', f)]=getattr(self, f)
        self.register(self, actions)

    @register(modes=['exec'])
    def installPicks(self): super().installPicks()

    @register(modes=['exec'])
    def updatePicks(self): super().updatePicks()

    @register('pc', modes=['normal', 'exec'])
    def cleanupPicks(self): 
        print('cleaning up')
        super().cleanupPicks()

    def add(self, picked):

        super().add(picked)
        if hasattr(picked, 'modeWanted'):
            picked.modeWanted.connect(self.set)
        if hasattr(picked, 'forceDelisten'):
            picked.forceDelisten.connect(self.set)
        if hasattr(picked, 'delistenWanted'):
            picked.delistenWanted.connect(self.set)
        if hasattr(picked, 'keysChanged'):
            picked.keysChanged.connect(self.keysChanged)

        self.register(picked, picked.actions)

    def set(self, listener='normal'):

        super().set(listener)
        self.modeChanged.emit(self.current)

    def register(self, plug, actions):

        super().register(plug, actions)
        self.actionsRegistered.emit()
