import re
from PyQt5 import QtCore, QtGui
from plug.qt import PlugObj

from .widget import ListWidget

class ExecList(PlugObj):

    def __init__(self, 
                 app=None, 
                 **kwargs,
                 ):

        super().__init__(
                app=app, 
                **kwargs,
                )

        self.setUI()
        self.clist=[]
        self.exec=None
        self.app.plugman.plugsLoaded.connect(
                self.on_plugsLoaded)

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
            exec_mode.tabPressed.connect(
                    self.on_tabPressed
                    )
            exec_mode.returnPressed.connect(
                    self.on_returnPressed
                    )
            exec_mode.textChanged.connect(
                    self.on_textChanged
                    )
            exec_mode.delistenWanted.connect(
                    self.on_delistenWanted
                    )
            exec_mode.startedListening.connect(
                    self.on_startedListening
                    )

    def on_startedListening(self):

        self.ui.show()
        self.on_textChanged()

    def on_delistenWanted(self):

        self.ui.hide()
        self.ui.model.clear()

    def on_tabPressed(self):

        if self.ui.proxy.rowCount()>1:

            idx=self.ui.list.currentIndex()
            text=idx.data()
            _, t, l=self.getEditText()
            new=' '.join(t[:-1]+[text])
            print(new)
            # self.setEditText(new)
            # todo edit loses focus

    def setEditText(self, text):

        self.app.window.bar.edit.setText(text)

    def getEditText(self):


        text=self.app.window.bar.edit.text()
        t=re.split('(\W)', text)
        return text, t, t[-1]

    def on_textChanged(self): 

        clist=[]
        text, t, last = self.getEditText()
        if len(t)==1:
            clist=self.exec.getSimilar(t[0])
            self.setList(clist)
        else:
            try:
                col = self.exec.getMethods()
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

        if clist:
            self.ui.proxy.clear()
            self.ui.model.clear()
            for i in clist:
                item=QtGui.QStandardItem(i)
                self.ui.model.appendRow(item)
            self.ui.list.setCurrentIndex(
                    self.ui.proxy.index(0, 0))

            edit=self.app.window.bar.edit
            cr=edit.cursorRect()
            self.ui.updatePosition(cr.x()+5)

    def on_returnPressed(self): 

        self.ui.hide()
