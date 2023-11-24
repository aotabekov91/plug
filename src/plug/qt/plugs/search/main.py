from PyQt5 import QtCore
from plug.qt import Plug
from gizmo.utils import tag
from gizmo.widget import ListWidget, ItemWidget

class Search(Plug):

    def __init__(
            self, 
            app,
            name='search',
            listen_leader='/', 
            show_statusbar=True,
            **kwargs
            ):

        super(Search, self).__init__(
                app=app, 
                name=name,
                listen_leader=listen_leader, 
                show_statusbar=show_statusbar, 
                **kwargs)

        self.index=-1
        self.matches=[]
        self.match=None
        self.setupUI()
        self.bar=app.ui.bar
        self.display=app.ui.display

    def setupUI(self):

        self.app.uiman.setupUI(self)
        lwid=ListWidget(
            check_fields=['up'],
            item_widget=ItemWidget)
        self.ui.addWidget(
                'main', lwid, main=True)

    @tag('l')
    def toggleList(self):

        if self.ui.isVisible():
            self.ui.deactivate()
        else:
            self.ui.activate()

    @tag('j')
    def next(self): 
        self.jump(+1)

    @tag('k')
    def prev(self): 
        self.jump(-1)

    @tag('f')
    def focusSearch(self): 
        self.bar.edit.setFocus()

    def listen(self): 

        super().listen()
        self.bar.edit.show()
        self.bar.edit.setFocus()
        self.bar.edit.returnPressed.connect(
                self.find)
        self.bar.hideWanted.connect(
                self.delistenWanted)

    def delisten(self):

        if self.listening:
            self.clear()
            self.ui.deactivate()
            self.bar.hideWanted.disconnect()
            self.bar.edit.returnPressed.disconnect(
                    self.find)
        super().delisten()

    def clear(self):

        self.index=-1
        self.match=None
        self.matches=[]
        view=self.display
        if view: 
            view.cleanUp()

    def find(self):

        def search(t, v, f=[]):
            if v:
                d=v.model()
                for p in d.pages().values():
                    rects=p.search(t)
                    if not rects: 
                        continue
                    for r in rects:
                        l=self.getLine(t, p, r)
                        f+=[{
                            'page': p.pageNumber(), 
                            'rect': r, 
                            'up': l 
                            }]
            return f

        v=self.display.view
        if not v:
            return
        t=self.bar.edit.text()
        m=search(t, v)
        self.matches=m
        self.clear()
        if len(m) > 0: 
            self.ui.main.setList(m)
            self.jump()
        else:
            m=[{'up': f'{t} not found'}]
            self.ui.main.setList(m)

    def jump(
            self, 
            increment=1,
            match=None
            ):

        v=self.display.view
        empty=len(self.matches)==0
        if empty or not v: 
            return
        if not match:
            self.index+=increment
            if self.index>=len(self.matches):
                self.index=0
            elif self.index<0:
                self.index=len(self.matches)-1
            match=self.matches[self.index]
            self.ui.main.setCurrentRow(
                    self.index)
        p=match['page']
        r=match['rect']
        i=v.pageItem(p-1)
        m=i.mapToItem(r)
        i.setSearched([m])
        y=i.mapRectToScene(m).y()
        v.goto(p)
        v.centerOn(0, y)

    def getLine(
            self, 
            text, 
            page, 
            rectF
            ):

        w=page.size().width()
        y, h =rectF.y(), rectF.height()
        lrect=QtCore.QRectF(0, y, w, h)
        l=f'<html>{page.find(lrect)}</html>'
        r=f'<font color="red">{text}</font>'
        return l.replace(text, r)
