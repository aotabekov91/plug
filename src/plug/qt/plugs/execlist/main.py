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

    def on_tabPressed(self): 

        col = self.exec.getMethods()

        clist=[]
        if not col:
            clist=self.exec.commands.keys()
        elif len(col)>1:
            clist=[c[0] for c in col]
        elif len(col)==1:
            n, m, a, u = col[0]
            c=self.exec.args[n]
            if u:
                last=u[-1]
                pos=len(u)-1

        if clist:
            self.ui.list.clear()
            self.ui.list.addItems(clist)
            self.ui.show()

    def on_returnPressed(self): 

        self.ui.hide()
