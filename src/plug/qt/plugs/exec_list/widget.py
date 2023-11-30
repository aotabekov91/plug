from PyQt5 import QtWidgets, QtCore, QtGui

class RunListWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.parent().installEventFilter(self)
        self.setup()

    def setup(self):

        self.list=QtWidgets.QListView(
                parent=self, objectName='List')
        self.list.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.list.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff)
        self.m_layout=QtWidgets.QVBoxLayout(self)
        self.m_layout.setContentsMargins(0,0,0,0)
        self.m_layout.addWidget(self.list)
        self.setLayout(self.m_layout)
        self.model=QtGui.QStandardItemModel()
        self.proxy=QtCore.QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.list.setModel(self.proxy)
        self.show()

    def show(self):

        super().show()
        self.list.show()

    def sizeHint(self):

        w=self.list.width()
        if self.proxy.rowCount()==0:
            return QtCore.QSize(w, 0)
        n=self.proxy.rowCount()
        h=self.list.sizeHintForRow(0)#*n

        c=0
        for i in range(self.proxy.rowCount()):
            c=max(c, self.list.sizeHintForColumn(i))
        c+=5

        r = self.parent().rect()

        dy=self.rect().y()
        w= min(int(0.8*r.width()-dy), c)
        h = min(int(0.9*r.height()), h*n)
        return QtCore.QSize(w, h) 

    def updatePosition(self, x=None):

        p = self.parent().rect()
        if p:
            self.adjustSize()
            w=self.width()
            h=self.height()
            if x is None: x=0
            y=p.height()-self.height()
            bar=self.parent().bar
            y-=25*bar.clayout.count()+2
            self.setGeometry(x, y, w, h)

    def eventFilter(self, widget, event):

        c1=event.type()==QtCore.QEvent.Resize
        if c1 and widget==self.parent():
            self.updatePosition()
            event.accept()
            return True
        return False
