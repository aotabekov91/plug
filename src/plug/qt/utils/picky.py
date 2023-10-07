from PyQt5 import QtCore
from gizmo.utils import register
from plug.utils.picky import Picky as Base

class Picky(Base, QtCore.QObject):

    def setup(self):

        super().setup()
        self.setActions()

    def setActions(self):

        funcs=[
                'installPicks', 
                'updatePicks', 
                'cleanupPicks', 
                'installRequirements'
               ]
        a={}
        for f in funcs:
            a[('Picky', f)]=getattr(self, f)
        self.moder.save(self, a)

    @register(modes=['exec'])
    def reloadPicks(self): 
        self.moder.load()

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
