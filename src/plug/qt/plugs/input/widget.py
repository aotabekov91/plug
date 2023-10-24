from PyQt5 import QtWidgets, QtCore 
from gizmo.widget import VimEditor as Base

class VimEditor(Base):

    def __init__(
            self, 
            *args, 
            **kwargs
            ):

        self.w_ratio=0.7
        self.h_ratio=0.7
        self.w_dratio=0.7
        self.h_dratio=0.7
        super().__init__(
                *args, **kwargs)

    def show(self):

        super().show()
        self.updatePosition()

    def updatePosition(self):

        r = self.parent().rect()
        pw=r.width()
        ph=r.height()
        w=int(pw*self.w_ratio)
        h=int(ph*self.h_ratio)
        x=int(pw/2-w/2)
        y=int(ph/2-h/2)
        self.setGeometry(x, y, w, h)

    # def setText(self, text):
    #     super().setText(text)
    #     self.adjustDocSize()

    # def adjustDocSize(self):
    #     doc=self.document()
    #     doc.adjustSize()

    def setRatio(self, w=None, h=None):

        self.w_ratio=self.w_dratio
        self.h_ratio=self.h_dratio
        if w: self.w_ratio=w
        if h: self.h_ratio=h
