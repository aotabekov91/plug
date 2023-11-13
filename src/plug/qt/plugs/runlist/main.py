from PyQt5 import QtGui
from plug.qt import Plug
from gizmo.utils import register

from .filler import Filler
from .widget import RunListWidget

class RunList(Plug):

    def __init__(
            self, 
            special=['tab'], 
            **kwargs
            ):

        self.args={}
        super().__init__(
                special=special,
                **kwargs,
                )
        self.filler=Filler()
        self.bar=self.app.window.bar
        self.app.moder.plugsLoaded.connect(
                self.setRunPlug)
        self.ear.tabPressed.connect(
                self.select)
        self.setUI()

    def setArgOptions(
            self, cname, aname, alist):

        if not cname in self.args:
            self.args[cname]={}
        self.args[cname][aname]=alist

    def setUI(self):

        self.ui=RunListWidget(
                    objectName='RunList',
                    parent=self.app.window
                    )
        self.ui.hide()

    def setRunPlug(self, plugs):

        self.run=plugs.get('run', None)
        if self.run:
            self.run.textChanged.connect(
                    self.updateText)
            self.run.startedListening.connect(
                    self.startListening)
            self.run.endedListening.connect(
                    self.stopListening)

    def startListening(self):

        self.ui.show()
        self.updateText()
        self.listen()

    def stopListening(self):

        self.ui.model.clear()
        self.ui.hide()
        self.delisten()

    @register('<c-l>')
    def select(self): 

        idx=self.ui.list.currentIndex()
        if idx.data():
            self.ui.list.setCurrentIndex(idx)
            text, tlist = self.current_data
            t=idx.data()
            new=''.join(tlist[:-1]+[t])
        self.setEditText(new)
        self.updateWidgetPosition()

    @register('<c-k>')
    def moveUp(self): 
        self.move('up')

    @register('<c-j>')
    def moveDown(self): 
        self.move('down')

    def move(self, kind):

        idx=self.ui.list.currentIndex()
        delta=1
        if kind=='up': delta=-1
        if idx.data():
            row=idx.row()+delta
        else:
            row=0
            if kind=='up':
                row=self.ui.proxy.rowCount()-1
        idx=self.ui.proxy.index(row, 0)
        self.ui.list.setCurrentIndex(idx)

    def setEditText(self, text):

        self.run.textChanged.disconnect(
                self.updateText)
        self.bar.edit.setText(text)
        self.run.textChanged.connect(
                self.updateText)

    def updateText(self): 

        clist=[]
        text, t, last = self.run.getEditText()
        self.current_data = text, t

        if len(t)==1:
            alist=self.run.commands
            clist=self.run.getSimilar(t[0], alist)
        else:

            try:
                col = self.run.getMethods() 
                if not col:
                    alist=self.run.commands
                    clist=self.run.getSimilar('', alist)
                else:
                    n, m, args, unk = col
                    found=None
                    for a, v in args.items():
                        if v.startswith(last):
                            found = (a, v)
                            break
                    if found: a, v = found
                    if not v: last=None
                    clist=self.getOptions(n, a, v)
            except ValueError as e:
                c, a=e.args
                clist=self.getOptions(c, a, last)
            # except Exception:
                # clist=None
            clist=self.getSimilar(last, clist)

        self.setList(clist)
        self.updateWidgetPosition()

    def getOptions(self, command, arg, last):

        cdict=self.args.get(command, None)
        if cdict:
            clist=self.args[command][arg]
            if clist=='path':
                clist=self.filler.getPaths(last)
            return clist

    def getSimilar(self, name, alist):

        if name: 
            alist=self.run.getSimilar(name, alist) 
        return alist

    def setList(self, clist):

        self.ui.proxy.clear()
        self.ui.model.clear()
        if clist:
            for item in clist:
                if type(item)!=QtGui.QStandardItem:
                    item=QtGui.QStandardItem(item)
                self.ui.model.appendRow(item)
            self.ui.list.setCurrentIndex(
                    self.ui.proxy.index(0, 0))
            self.updateWidgetPosition()

    def updateWidgetPosition(self, x=None, delta=5):

        cx=self.bar.edit.cursorRect().x()+delta
        self.ui.updatePosition(x or cx)
