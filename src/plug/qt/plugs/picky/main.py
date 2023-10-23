from PyQt5 import QtCore
from gizmo.utils import register
from plug.plugs.picky import Picky as Base

class Picky(Base, QtCore.QObject):

    @register(modes=['run'])
    def reloadPicks(self): 
        self.moder.load()

    @register(modes=['run'])
    def installPicks(self): 
        super().installPicks()

    @register(modes=['run'])
    def installRequirements(self):
        super().installRequirements()

    @register(modes=['run'])
    def updatePicks(self): 
        super().updatePicks()

    @register(modes=['run'])
    def cleanupPicks(self): 
        super().cleanupPicks()
