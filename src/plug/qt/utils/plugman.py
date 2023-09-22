from PyQt5 import QtCore

from plug.utils import Plugman as Base

class Plugman(Base, QtCore.QObject):

    keysChanged=QtCore.pyqtSignal(str)
    modeChanged=QtCore.pyqtSignal(object)
    plugAdded=QtCore.pyqtSignal(object)
    plugsLoaded=QtCore.pyqtSignal(object)
    actionsRegistered=QtCore.pyqtSignal(
            object, object)

    def setup(self):

        super().setup()
        funcs=['installPicks', 
               'updatePicks', 
               'cleanupPicks',
               'installRequirements'
               ]
        a={}
        for f in funcs:
            a[('Plugman', f)]=getattr(self, f)
        self.register(self, a)

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
        self.plugAdded.emit(picked)

    def loadPlugs(self, plugs):

        super().loadPlugs(plugs)
        self.plugsLoaded.emit(self.plugs)

    def set(self, listener='normal'):

        super().set(listener)
        self.modeChanged.emit(self.current)

    def register(self, plug, actions):

        super().register(plug, actions)
        self.actionsRegistered.emit(plug, actions)
