from PyQt5 import QtCore

from plug.utils import Plugman as Base
from plug.qt.utils.register import register

class Plugman(Base, QtCore.QObject):

    keysChanged=QtCore.pyqtSignal(str)
    modeChanged=QtCore.pyqtSignal(object)
    plugLoaded=QtCore.pyqtSignal(object)
    plugsLoaded=QtCore.pyqtSignal(object)
    actionsRegistered=QtCore.pyqtSignal(object, object)

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
    def installPicks(self): 

        super().installPicks()

    @register(modes=['exec'])
    def updatePicks(self): 

        super().updatePicks()

    @register(modes=['normal', 'exec'])
    def cleanupPicks(self): 

        super().cleanupPicks()

    @register(modes=['normal', 'exec'])
    def loadPicks(self):

        super().loadPicks()

    def add(self, picked):

        super().add(picked)
        if hasattr(picked, 'modeWanted'):
            picked.modeWanted.connect(
                    self.set)
        if hasattr(picked, 'forceDelisten'):
            picked.forceDelisten.connect(
                    self.set)
        if hasattr(picked, 'delistenWanted'):
            picked.delistenWanted.connect(
                    self.set)
        if hasattr(picked, 'keysChanged'):
            picked.keysChanged.connect(
                    self.keysChanged)

        self.register(picked, picked.actions)
        self.plugLoaded.emit(picked)

    def loadPlugs(self, plugs):

        super().loadPlugs(plugs)
        self.plugsLoaded.emit(self.plugs)

    def set(self, listener='normal'):

        super().set(listener)
        self.modeChanged.emit(self.current)

    def register(self, plug, actions):

        super().register(plug, actions)
        self.actionsRegistered.emit(plug, actions)
