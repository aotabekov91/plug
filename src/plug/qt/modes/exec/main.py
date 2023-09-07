from PyQt5 import QtCore
from argparse import ArgumentError
from collections import OrderedDict
from inspect import signature, Parameter

from plug.qt import PlugObj
from .parser import ArgumentParser

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
        self.event_listener.tabPressed.connect(
                self.on_tabPressed)
        self.event_listener.keysSet.connect(
                self.on_keysSet)

    def setup(self):

        super().setup()
        self.setParser()

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

    def setParser(self):

        self.parser=ArgumentParser()
        self.subparser=self.parser.add_subparsers(
                dest='command'
                )

    def on_keysSet(self, commands):

        self.commands = self.event_listener.methods
        for c, m in self.commands.items():
            self.args[c]=OrderedDict()
            prmts=signature(m).parameters
            parser=self.subparser.add_parser(c)
            for n, p in prmts.items():
                self.args[c][n]=[]
                if p.default==Parameter.empty:
                    parser.add_argument(n)
                else:
                    parser.add_argument(
                            f'--{n}',
                            default=p.default)


    def on_tabPressed(self):

        edit=self.app.window.bar.edit
        t=edit.text().split(' ')

        if len(t)==1:
            similar=self.getSimilar(t[0])
            if len(similar)==1:
                n = similar[0]
                edit=self.app.window.bar.edit
                edit.setText(f'{n} ')
                edit.setFocus()

        self.tabPressed.emit()

    def on_returnPressed(self): 

        try:
            col=self.getMethods()
            if len(col)==1: 
                _, m, kw, pos = col[0]
                args={k:v for k, v in kw.items() if v}
                m(*pos, **args)
        except:
            pass

        self.delistenWanted.emit()

    def parse(self, t=None):

        if not t:
            t=self.app.window.bar.edit.text().strip()
        args, unkwn = super().parse(t)
        return args, unkwn

    def getCollection(self, command, args, unkwn):

        col = []
        for n, m in self.commands.items():
            if n[:len(command)]!=command: 
                continue
            args=OrderedDict()
            for a, v in args.items():
                c1 = a in self.args[n]
                if c1: args[a]=v
            col+=[(n, m, args, unkwn)]
            if n==command: break
        return col

    def getSimilar(self, c):

        similar=[]
        for n, m in self.commands.items():
            if n[:len(c)]!=c: continue
            similar+=[n]
        return similar

    def getMethodByAlias(self, c):

        similar=self.getSimilar(c)
        if len(similar)!=1: return []

        n=similar[0]
        t=self.app.window.bar.edit.text().strip()
        t=t.replace(c, n, 1)
        args, unkwn = self.parse(t)
        c=args.command
        args=vars(args)
        col=self.getCollection(c, args, unkwn)
        return col

    def getMethodByName(self):

        args, unkwn = self.parse()
        c=args.command
        args=vars(args)
        return self.getCollection(
                c, args, unkwn)

    def getMethods(self):

        try:
            return self.getMethodByName()
        except LookupError as e:
            return self.getMethodByAlias(
                    e.args[0])
