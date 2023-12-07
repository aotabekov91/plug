from plug.qt import Plug
from PyQt5 import QtWidgets, QtCore

class Follow(Plug):

    labels={}
    name='hint'
    isMode=True
    style='color: green'
    listen_leader='<c-f>'

    def event_functor(self, e, ear):

        n=e.text()
        d=self.labels.get(n, None)
        self.octivate()
        if d: 
            v, l = d
            v.setFocus()
        return True

    def activate(self):

        super().activate()
        self.hint()

    def octivate(self):

        super().octivate()
        self.app.earman.clearKeys(
                clear_text=True)
        self.dehint()

    def mapToUI(self, c, ui):

        p=ui.parent()
        if not p: return c
        c=ui.mapToParent(c)
        return self.mapToUI(c, p)

    def hint(self):

        def pos_sort(v):

            c=QtCore.QPoint(1, 1)
            c=self.mapToUI(c, v)
            return (c.x(), c.y())

        self.labels={}
        a=self.app.uiman.active()
        visible=[]
        for f in a.values():
            if not f.isVisible(): continue
            if self.checkProp('canFollow', f):
                visible+=[f]
        if not visible: self.octivate()
        slist=sorted(visible, key=pos_sort)

        for i, n in enumerate(slist):
            l=QtWidgets.QLabel(
                    str(i+1), 
                    parent=self.app.ui,
                    objectName='HintLabel',
                    )
            idx=str(i+1)
            self.labels[idx]=(n, l)
            l.setAlignment(QtCore.Qt.AlignCenter)
            c=QtCore.QPoint(1, 1)
            c=self.mapToUI(c, n)
            r=n.rect()
            x, y = c.x()-1, c.y()-1
            w, h = r.width(), r.height() 
            l.setGeometry(x, y, w, h)
            s=f'{self.style}; font-size: {min(w, h)}px'
            l.setStyleSheet(s)
            l.show()

    def dehint(self):

        for i, (n, l) in self.labels.items():
            l.hide()
            l.setParent(None)
