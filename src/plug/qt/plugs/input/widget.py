from PyQt5 import QtWidgets, QtCore 

from gizmo.widget import VimEditor, NVim

class InputWidget(QtWidgets.QWidget):

    modeChanged=QtCore.pyqtSignal(object)

    def __init__(self, parent):

        self.app=parent
        super().__init__(
                objectName='Input',
                parent=self.app.window.main,
                )
        self.setup()
        self.parent().installEventFilter(self)

    def setText(self, text):

        self.nvim.setText(text)
        self.field.setText(text)

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

    def updatePosition(self):

        parent_rect = self.parent().rect()

        if parent_rect:

            pwidth=parent_rect.width()
            pheight=parent_rect.height()

            w=int(pwidth*0.7)
            h=int(pheight*0.7)

            self.setFixedSize(w, h)

            x=int(pwidth/2-self.width()/2)
            y=int(pheight/2-self.height()/2)

            self.setGeometry(x, y, w, h)

    def eventFilter(self, widget, event):

        c1=event.type()==QtCore.QEvent.Resize
        if c1:
            if widget==self.parent():
                self.updatePosition()
                event.accept()
                return True
        return False
