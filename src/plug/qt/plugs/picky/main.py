from PyQt5 import QtCore
from gizmo.utils import tag
from plug.plugs.picky import Picky as Base

class Picky(Base, QtCore.QObject):

    @tag(modes=['exec'])
    def reloadPicks(self): 
        self.moder.load()

    @tag(modes=['exec'])
    def installPicks(self): 
        super().installPicks()

    @tag(modes=['exec'])
    def installRequirements(self):
        super().installRequirements()

    @tag(modes=['exec'])
    def updatePicks(self): 
        super().updatePicks()

    @tag(modes=['exec'])
    def cleanupPicks(self): 
        super().cleanupPicks()
