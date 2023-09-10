from PyQt5 import QtCore
from collections import OrderedDict
from inspect import signature, Parameter

from plug.qt import PlugObj
from .parser import ArgumentParser

class Exec(PlugObj):

    special=['return', 
             'tab', 
             'carriage', 
             'escape', 
             'escape_bracket']

    tabPressed=QtCore.pyqtSignal()
    textChanged=QtCore.pyqtSignal()

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

        self.commands={}
        self.event_listener.returnPressed.connect(
                self.on_returnPressed)
        self.event_listener.carriageReturnPressed.connect(
                self.on_returnPressed)
        self.event_listener.tabPressed.connect(
                self.on_tabPressed)
        self.event_listener.keysSet.connect(
                self.on_keysSet)

    def setup(self):

        super().setup()
        self.setParser()

    def delisten(self):

        super().delisten()
        bar=self.app.window.bar
        bar.bottom.hide()
        bar.edit.textChanged.disconnect(
                self.textChanged)
        bar.edit.clear()

    def listen(self):

        super().listen()
        bar=self.app.window.bar
        bar.bottom.show()
        bar.show()
        bar.edit.setFocus()
        bar.edit.textChanged.connect(
                self.textChanged)

    def setParser(self):

        self.parser=ArgumentParser()
        self.subparser=self.parser.add_subparsers(
                dest='command'
                )

    def on_keysSet(self, commands):

        self.commands = self.event_listener.methods
        for c, m in self.commands.items():
            prmts=signature(m).parameters
            parser=self.subparser.add_parser(c)
            for n, p in prmts.items():
                if p.default==Parameter.empty:
                    parser.add_argument(n)
                else:
                    parser.add_argument(
                            f'--{n}',
                            default=p.default)

    def on_tabPressed(self): pass

    def on_returnPressed(self): 


        try:
            text=self.app.window.bar.edit.text().strip()
            if text:
                col=self.getMethods()
                if col:
                    n, m, args, unk = col
                    m(**args)
        except:
            pass
        self.delistenWanted.emit()

    def parse(self, text=None):

        if not text:
            text=self.app.window.bar.edit.text().strip()
        args, unkwn = super().parse(text)
        return args, unkwn

    def getSimilar(self, c, olist):

        similar=[]
        for n in olist:
            if n.startswith(c): 
                similar+=[n]
        return similar

    def getMethodByAbbv(self, c):

        alist=self.commands.keys()
        similar=self.getSimilar(c, alist)
        if len(similar)!=1: 
            return None 
        n=similar[0]
        t=self.app.window.bar.edit.text().strip()
        t=t.replace(c, n, 1)
        return self.getMethodByName(t)

    def getMethodByName(self, text=None):

        args, unkwn = self.parse(text)
        args=vars(args)
        n=args.pop('command', None)
        m=self.commands.get(n, None)
        if m: return (n, m, args, unkwn)

    def getMethods(self):

        try:
            return self.getMethodByName()
        except LookupError as e:
            return self.getMethodByAbbv(
                    e.args[0])
        except:
            return None
