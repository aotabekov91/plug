import re
import shlex
from PyQt5 import QtCore
from inspect import signature, Parameter

from plug.qt import Plug
from .parser import ArgumentParser

class Run(Plug):

    special=[
            'return', 
            'tab', 
            'carriage', 
            'escape', 
            'escape_bracket'
            ]
    textChanged=QtCore.pyqtSignal()

    def __init__(
            self, 
            app=None, 
            name='run', 
            special=special, 
            listen_leader='<c-r>', 
            **kwargs
            ):

        self.commands={}
        super().__init__(
                app=app, 
                name=name, 
                special=special,
                listen_leader=listen_leader, 
                **kwargs
                )

        self.ear.returnPressed.connect(
                self.on_returnPressed)
        self.ear.carriageReturnPressed.connect(
                self.on_returnPressed)
        self.ear.tabPressed.connect(
                self.on_tabPressed)
        self.ear.keysSet.connect(
                self.on_keysSet)

    def setup(self):

        super().setup()
        self.setParser()
        if self.app:
            self.app.moder.plugsLoaded.connect(
                    self.on_plugsLoaded
                    )

    def on_plugsLoaded(self, plugs):

        self.functions.update(
                self.commands)

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
                dest='command')

    def on_keysSet(self, commands):

        for c, m in self.ear.methods.items():
            if c in self.commands: 
                continue
            self.commands[c]=m
            prmts=signature(m).parameters
            parser=self.subparser.add_parser(c)
            for n, p in prmts.items():
                try:

                    if p.default==Parameter.empty:
                        parser.add_argument(n)
                    else:
                        parser.add_argument(
                                f'--{n}',
                                default=p.default)
                except:
                    pass

    def on_tabPressed(self): pass

    def on_returnPressed(self): 

        # try:

        text, _, __=self.getEditText()
        if text:
            col=self.getMethods()
            if col:
                n, m, args, unk = col
                m(**args)

        # except:
        #     pass

        self.delistenWanted.emit()

    def getEditText(self):

        text=self.app.window.bar.edit.text()
        t=re.split('( )', text)
        self.current_data=text, t
        return text, t, t[-1]

    def parse(self, t=None):

        if not t:
            t, _, __ = self.getEditText()
        t=shlex.split(t)
        return self.parser.parse_known_args(t)

    def getSimilar(self, c, alist):

        s=[]
        if not alist: return s
        for n in alist:
            if n.startswith(c): s+=[n]
        return s

    def getMethodByAbbv(self, c):

        alist=self.commands.keys()
        similar=self.getSimilar(c, alist)
        if len(similar)!=1: return None 
        n=similar[0]
        t, _, __ = self.getEditText()
        t=t.replace(c, n, 1)
        return self.getMethodByName(t)

    def getMethodByName(self, text=None):

        a, u = self.parse(text)
        a=vars(a)
        n=a.pop('command', None)
        m=self.commands.get(n, None)
        if m: 
            return (n, m, a, u)

    def getMethods(self, raise_error=True):

        try:
            return self.getMethodByName()
        except LookupError as e:
            return self.getMethodByAbbv(
                    e.args[0])
        except:
            if raise_error:
                raise
            else:
                return None
