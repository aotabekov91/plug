from PyQt5 import QtGui

from plug.qt import Plug
from plug.utils import register

from .filler import Filler
from .widget import ListWidget

class ExecList(Plug):

    def __init__(self, 
                 app=None, 
                 special=['tab'],
                 **kwargs,
                 ):

        super().__init__(
                app=app, 
                special=special,
                **kwargs,
                )

        self.setUI()
        self.args={}
        self.exec=None
        self.filler=Filler()

    def setup(self):

        super().setup()
        self.setConnect()

    def setConnect(self):

        self.app.plugman.plugsLoaded.connect(
                self.on_plugsLoaded)
        self.ear.tabPressed.connect(
                self.select)

    def setArgOptions(self, 
                      cname, 
                      aname, 
                      alist):
        if not cname in self.args:
            self.args[cname]={}
        self.args[cname][aname]=alist

    def setUI(self):

        self.ui=ListWidget(
                    objectName='ExecList',
                    parent=self.app.window,
                )
        self.ui.hide()

    def on_plugsLoaded(self, plugs):

        exec_mode=plugs.get('exec', None)
        if exec_mode:
            self.exec=exec_mode
            exec_mode.textChanged.connect(
                    self.on_textChanged
                    )
            exec_mode.startedListening.connect(
                    self.on_startedListening
                    )
            exec_mode.endedListening.connect(
                    self.on_delistenWanted
                    )

    def on_startedListening(self):

        self.ui.show()
        self.on_textChanged()
        self.listen()

    def on_delistenWanted(self):

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
        self.updateListPosition()

    @register('<c-k>')
    def moveUp(self): self.move('up')

    @register('<c-j>')
    def moveDown(self): self.move('down')

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

        self.exec.textChanged.disconnect(
                self.on_textChanged)
        self.app.window.bar.edit.setText(text)
        self.exec.textChanged.connect(
                self.on_textChanged)

    def on_textChanged(self): 

        clist=[]
        text, t, last = self.exec.getEditText()
        self.current_data = text, t

        if len(t)==1:
            alist=self.exec.commands
            clist=self.exec.getSimilar(t[0], alist)
        else:

            try:
                col = self.exec.getMethods() 
                if not col:
                    alist=self.exec.commands
                    clist=self.exec.getSimilar('', alist)
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
        self.updateListPosition()

    def getOptions(self, command, arg, last):

        cdict=self.args.get(command, None)
        if cdict:
            clist=self.args[command][arg]
            if clist=='path':
                clist=self.filler.getPaths(last)
            return clist

    def getSimilar(self, name, alist):

        if not name: return alist
        return self.exec.getSimilar(name, alist)

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
            self.updateListPosition()

    def updateListPosition(self, x=None, delta=5):

        if not x:
            edit=self.app.window.bar.edit
            x=edit.cursorRect().x()+delta
        self.ui.updatePosition(x)
