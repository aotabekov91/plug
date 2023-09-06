from PyQt5 import QtCore
from inspect import signature
from collections import OrderedDict

from plug.qt import PlugObj

class Exec(PlugObj):

    special=['return', 
            'carriage', 
            'escape', 
            'escape_bracket']

    tabPressed=QtCore.pyqtSignal()

    def __init__(self, 
                 app=None, 
                 name='exec',
                 special=special,
                 listen_leader='<c-e>',
                 **kwargs
                 ):

        super().__init__(
                app=app, 
                name=name, 
                special=special,
                listen_leader=listen_leader, 
                **kwargs
                )
        self.args={}
        self.options={}
        self.commands={}
        self.event_listener.returnPressed.connect(
                self.on_returnPressed)
        self.event_listener.keysSet.connect(
                self.on_keysSet)

    def setup(self):

        super().setup()
        self.setParser()
        self.parser.add_argument('command')

    def delisten(self):

        super().delisten()
        self.app.window.bar.bottom.hide()
        self.app.window.bar.edit.clear()

    def listen(self):

        super().listen()
        self.app.window.bar.show()
        self.app.window.bar.bottom.show()
        self.app.window.bar.edit.setFocus()

    def addOptions(self, name, option_list):

        self.options[name]=option_list

    def on_keysSet(self, commands):

        self.commands = self.event_listener.methods
        for c, m in self.commands.items():
            self.args[c]=OrderedDict()
            prmts=signature(m).parameters
            self.args[c]={}
            for n, p in prmts.items():
                self.args[c][n]=[]
                self.parser.add_argument(
                        f'--{p}')

                # if p.default!=Parameter.empty:
                #     self.parser.add_argument(f'--{p}')
                # else:
                #     self.parser.add_argument(f'--{p}')

    def on_tabPressed(self):

        self.tabPressed.emit()

    def on_returnPressed(self): 

        col=self.getMethods()
        if len(col)==1: 
            _, m, kwargs, pos = col[0]
            m(*pos, **kwargs)
        self.delistenWanted.emit()

    def getText(self):

        t=self.app.window.bar.edit.text()
        return self.parse(t)

    def getMethods(self):

        col=[]
        args, unkwn = self.getText()
        t=args.command
        for n, m in self.commands.items():
            if n[:len(t)]!=t: continue
            aa={}
            for a, v in vars(args).items():
                c1 = a in self.args[n]
                c2 = not v is None
                if c1 and c2: aa[a]=v
            col+=[(n, m, aa, unkwn)]
            if n==t: break
        return col
