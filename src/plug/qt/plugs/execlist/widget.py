from PyQt5 import QtWidgets, QtCore, QtGui

class ListWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.setup()
        self.parent().installEventFilter(self)

    def setup(self):

        self.list=QtWidgets.QListView(
                parent=self,
                objectName='List',
                )

        self.model=QtGui.QStandardItemModel()
        self.proxy=QtCore.QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.list.setModel(self.proxy)

        self.show()

    def show(self):

        super().show()
        self.list.show()

    def sizeHint(self):

        w=self.width()
        if self.proxy.rowCount()==0:
            return QtCore.QSize(w, 0)
        n=self.proxy.rowCount()
        h=self.list.sizeHintForRow(0)
        ph = self.parent().rect().height()
        h=min(ph, h*n)
        return QtCore.QSize(w, h) 

    def updatePosition(self, x=None):

        prect = self.parent().rect()
        if prect:
            self.adjustSize()
            w=self.width()
            h=self.height()
            if x is None: x=0
            y=prect.height()-self.height()
            self.setGeometry(x, y, w, h)

    def eventFilter(self, widget, event):

        c1=event.type()==QtCore.QEvent.Resize
        if c1 and widget==self.parent():
            self.updatePosition()
            event.accept()
            return True
        return False
