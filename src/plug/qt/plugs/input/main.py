from plug.qt import Plug
from gizmo.utils import tag
from PyQt5 import QtCore, QtWidgets, QtGui

class Input(Plug):

    name='input'
    style='color: white'
    listen_leader='<c-i>'

    def activateWidget(self, w):

        self.pint()
        self.setSubmode('edit')
        self.app.earman.setPassive(
                True, modes=['input'])
        w.setFocus()

    @tag('a', modes=['input[hint]'])
    def append(self, digit=1):

        w=self.insert(digit)
        if w:
            cur=w.textCursor()
            cur.movePosition(
                    QtGui.QTextCursor.End)
            w.setTextCursor(cur)
            return w

    @tag('i', modes=['input[hint]'])
    def insert(self, digit=1):

        self.pint()
        d=self.labels.get(digit, None)
        if d: 
            w, l = d
            self.activateWidget(w)
            return w

    def hintAll(self):

        self.setSubmode('hint')
        def pos_sort(v):

            c=QtCore.QPoint(1, 1)
            c=self.mapToUI(c, v)
            return (c.x(), c.y())

        a=self.widgets
        visible=[f for f in a if f.isVisible()]
        slist=sorted(visible, key=pos_sort)

        for i, n in enumerate(slist):
            l=QtWidgets.QLabel(
                    str(i+1), 
                    parent=self.app.ui,
                    objectName='HintLabel',
                    )
            self.labels[i+1]=(n, l)
            l.setAlignment(QtCore.Qt.AlignLeft)
            c=QtCore.QPoint(1, 1)
            c=self.mapToUI(c, n)
            r=n.rect()
            x, y = c.x(), c.y()
            w, h = r.width(), r.height() 
            l.setGeometry(x, y, w, h)
            s=f'{self.style}; font-size: {min(w, h)}px; background-color: green;'
            l.setStyleSheet(s)
            l.show()

    def pint(self):

        for i, (n, l) in self.labels.items():
            l.hide()
            l.setParent(None)

    def mapToUI(self, c, ui):

        p=ui.parent()
        if not p: return c
        c=ui.mapToParent(c)
        return self.mapToUI(c, p)

    def setInputWidgets(self):

        w=[]
        self.labels={}
        v=self.app.handler.view()
        if self.checkProp('canInput', v):
            w=v.inputGetWidgets()
        self.widgets=w
        if not w: self.octivate()

    def octivate(self):

        self.pint()
        super().octivate()
        self.app.earman.setPassive(False)

    def activate(self):

        super().activate()
        self.setInputWidgets()
        self.hintAll()
