import re
from PyQt5 import QtGui

from plug.qt import PlugObj
from plug.qt.utils import register

from .widget import ListWidget

class ExecList(PlugObj):

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
        self.clist=[]
        self.exec=None
        self.app.plugman.plugsLoaded.connect(
                self.on_plugsLoaded)

        self.event_listener.tabPressed.connect(
                self.select)

    def on_tabPressed(self): raise

    def setUI(self):

        self.ui=ListWidget(
                    objectName='ExecList',
                    parent=self.app.window.main,
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

        self.exec.textChanged.disconnect(
                self.on_textChanged)
        self.setEditText(new)
        self.exec.textChanged.connect(
                self.on_textChanged)
        self.setEditText(new+' ')
        self.updateListPosition()

    @register('<c-k>')
    def moveUp(self): self.move('up')

    @register('<c-j>')
    def moveDown(self): self.move('down')

    def move(self, kind):

        idx=self.ui.list.currentIndex()

        if kind=='up':
            delta=-1
        else:
            delta=1

        if idx.data():
            row=idx.row()+delta
            idx=self.ui.proxy.index(row, 0)
            self.ui.list.setCurrentIndex(idx)
            text, tlist = self.current_data
            t=idx.data()
            if t:
                new=''.join(tlist[:-1]+[t])
            else:
                new=''.join(tlist)
        else:
            if kind=='up':
                row=self.ui.proxy.rowCount()-1
            else:
                row=0
            idx=self.ui.proxy.index(row, 0)
            self.ui.list.setCurrentIndex(idx)
            text, tlist = self.current_data
            t=idx.data()
            new=''.join(tlist[:-1]+[t])

        self.exec.textChanged.disconnect(
                self.on_textChanged)
        self.setEditText(new)
        self.exec.textChanged.connect(
                self.on_textChanged)

    def setEditText(self, text):

        self.app.window.bar.edit.setText(text)

    def getEditText(self):

        text=self.app.window.bar.edit.text()
        t=re.split('(\W)', text)
        self.current_data=text, t
        return text, t, t[-1]

    def on_textChanged(self): 

        clist=[]
        text, t, last = self.getEditText()

        if len(t)==1:
            clist=self.exec.getSimilar(t[0])
            self.setList(clist)
        else:
            try:
                try:
                    col = self.exec.getMethodByName()
                except LookupError as e:
                    col = self.exec.getMethodByAlias(
                            e.args[0])
                if not col:
                    clist=self.exec.getSimilar('')
                else:
                    n, m, args, unk = col
                    found=None
                    for a, v in args.items():
                        if v.startswith(last):
                            found = (a, v)
                            break
                    if found:
                        a, v = found
                        clist=self.exec.args[n][a]
            except ValueError as e:
                command, arg=e.args
                clist=self.exec.args[command][arg]
            except Exception as e:
                clist=[]
            clist=self.getSimilar(last, clist)
            self.setList(clist)

    def getSimilar(self, name, alist):

        if not name: return alist

        similar=[]
        for a in alist:
            if a.startswith(name): 
                similar+=[a]
        return similar

    def setList(self, clist):

        self.ui.proxy.clear()
        self.ui.model.clear()

        if clist:
            for i in clist:
                item=QtGui.QStandardItem(i)
                self.ui.model.appendRow(item)
            self.ui.list.setCurrentIndex(
                    self.ui.proxy.index(0, 0))
            self.updateListPosition()

    def updateListPosition(self, x=None):

        if not x:
            edit=self.app.window.bar.edit
            cr=edit.cursorRect()
            x=cr.x()+5
        self.ui.updatePosition(x)
