from PyQt5 import QtWidgets, QtCore 

class ListWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.setup()
        self.parent().installEventFilter(self)

    def setup(self):

        self.list=QtWidgets.QListWidget(
                parent=self,
                objectName='List',
                )
        self.show()
        self.list.show()

    def updatePosition(self):

        prect = self.parent().rect()
        if prect:
            w=self.list.width()
            h=self.list.height()
            x=0
            y=prect.height()-self.list.height()
            self.setGeometry(x, y, w, h)

    def eventFilter(self, widget, event):

        c1=event.type()==QtCore.QEvent.Resize
        if c1 and widget==self.parent():
            self.updatePosition()
            event.accept()
            return True
        return False
