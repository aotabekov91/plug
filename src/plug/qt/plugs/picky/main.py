from PyQt5 import QtCore
from gizmo.utils import tag
from plug.plugs.picky import Picky as Base

class Picky(Base, QtCore.QObject):

    @tag(modes=['run'])
    def reloadPicks(self): 
        self.moder.load()

    @tag(modes=['run'])
    def installPicks(self): 
        super().installPicks()

    @tag(modes=['run'])
    def installRequirements(self):
        super().installRequirements()

    @tag(modes=['run'])
    def updatePicks(self): 
        super().updatePicks()

    @tag(modes=['run'])
    def cleanupPicks(self): 
        super().cleanupPicks()
