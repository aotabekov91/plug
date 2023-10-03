from PyQt5 import QtCore

from gizmo.utils import register
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
        self.saveActions(self, a)

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
        self.saveActions(picked, picked.actions)
        self.plugAdded.emit(picked)

    def loadPlugs(self, plugs):

        super().loadPlugs(plugs)
        self.plugsLoaded.emit(self.plugs)

    def set(self, listener='normal'):

        super().set(listener)
        self.modeChanged.emit(self.current)

    def saveActions(self, plug, actions):

        super().saveActions(plug, actions)
        self.actionsRegistered.emit(plug, actions)

    @register(modes=['exec'])
    def installPicks(self): 
        super().installPicks()

    @register(modes=['exec'])
    def installRequirements(self):
        super().installRequirements()

    @register(modes=['exec'])
    def updatePicks(self): 
        super().updatePicks()

    @register(modes=['exec'])
    def cleanupPicks(self): 
        super().cleanupPicks()
