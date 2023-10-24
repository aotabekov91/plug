from PyQt5 import QtWidgets, QtCore 
from gizmo.widget import VimEditor, NVim

class InputWidget(QtWidgets.QWidget):

    modeChanged=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            *args, 
            objectName='Input',
            **kwargs
            ):

        self.w_ratio=0.7
        self.h_ratio=0.7
        self.w_dratio=0.7
        self.h_dratio=0.7
        super().__init__(
                *args,
                objectName=objectName,
                **kwargs
                )
        self.setup()

    def setRatio(self, w=None, h=None):

        self.w_ratio=self.w_dratio
        self.h_ratio=self.h_dratio
        if w: self.w_ratio=w
        if h: self.h_ratio=h

    def setText(self, text):

        self.nvim.setText(text)
        self.field.setText(text)
        doc=self.field.document()
        doc.adjustSize()

    def setup(self):

        self.nvim=NVim()
        self.label=QtWidgets.QLabel()
        self.field=VimEditor(
                nvim=self.nvim, 
                )
        self.field.modeChanged.connect(
                self.modeChanged)
        layout=QtWidgets.QVBoxLayout()
        layout.setSpacing(5)
        layout.addWidget(self.label)
        layout.addWidget(self.field)
        self.setLayout(layout)
        self.setAttribute(
                QtCore.Qt.WA_TranslucentBackground)
        self.label.hide()
        self.field.hide()

    def show(self):

        super().show()
        self.updatePosition()

    def updatePosition(self):

        r = self.parent().rect()
        if r:
            pw=r.width()
            ph=r.height()
            w=int(pw*self.w_ratio)
            h=int(ph*self.h_ratio)
            x=int(pw/2-w/2)
            y=int(ph/2-h/2)
            self.setGeometry(x, y, w, h)
