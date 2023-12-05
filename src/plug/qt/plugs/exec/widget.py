from PyQt5 import QtCore 
from gizmo.utils import tag
from gizmo.vimo.view import ListView

class ExecList(ListView):

    @tag('<c-j>', modes=['exec|ExecList'])
    def goToDown(self):
        super().goToDown()

    @tag('<c-k>', modes=['exec|ExecList'])
    def goToUp(self):
        super().goToUp()

    @tag('<c-l>gg', modes=['exec|ExecList'])
    def goToFirst(self):
        super().goToFirst()

    @tag('<c-l>G', modes=['exec|ExecList'])
    def goTo(self, digit=None):
        super().goTo(digit)

    def sizeHint(self):

        w=self.width()
        if self.m_model.rowCount()==0:
            return QtCore.QSize(w, 0)
        n=self.m_model.rowCount()
        h=self.sizeHintForRow(0)#*n

        c=0
        for i in range(self.m_model.rowCount()):
            c=max(c, self.sizeHintForColumn(i))
        c+=5
        r = self.parent().rect()
        dy=self.rect().y()
        w= min(int(0.8*r.width()-dy), c)
        h = min(int(0.9*r.height()), h*n)
        return QtCore.QSize(w, h) 

    def updatePosition(self, x=None):

        bar = self.bar
        p = self.parent().rect()
        if p:
            self.adjustSize()
            w=self.width()
            h=self.height()
            if x is None: x=0
            y=p.height()-self.height()-2
            c=bar.clayout.count()
            for i in range(c):
                i=bar.clayout.itemAt(i)
                iw=i.widget()
                if iw.isVisible(): y-=25
            self.setGeometry(x, y, w, h)
