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
            special=special, 
            listen_leader='<c-r>', 
            **kwargs
            ):

        self.commands={}
        super().__init__(
                name='run',
                special=special,
                listen_leader=listen_leader, 
                **kwargs)
        self.ear.returnPressed.connect(
                self.on_returnPressed)
        self.ear.carriageReturnPressed.connect(
                self.on_returnPressed)
        self.ear.tabPressed.connect(
                self.on_tabPressed)
        self.ear.keysSet.connect(
                self.updateKeysSet)

    def setup(self):

        super().setup()
        self.setParser()
        self.bar=self.app.window.bar
        self.app.moder.plugsLoaded.connect(
                self.setModeFunctions)

    def setModeFunctions(self, plugs):
        self.funcs.update(self.commands)

    def delisten(self):

        super().delisten()
        self.bar.bottom.hide()
        self.bar.edit.textChanged.disconnect(
                self.textChanged)
        self.bar.edit.clear()

    def listen(self):

        super().listen()
        self.bar.bottom.show()
        self.bar.show()
        self.bar.edit.setFocus()
        self.bar.edit.textChanged.connect(
                self.textChanged)

    def setParser(self):

        self.parser=ArgumentParser()
        self.subparser=self.parser.add_subparsers(
                dest='command')

    def updateKeysSet(self, commands):

        for c, m in self.ear.methods.items():
            if c in self.commands: 
                continue
            self.commands[c]=m
            prmts=signature(m).parameters
            p=self.subparser.add_parser(c)
            for n, v in prmts.items():
                try:
                    if v.default==Parameter.empty:
                        p.add_argument(n)
                    else:
                        p.add_argument(
                                f'--{n}', default=v.default)
                except:
                    pass

    def on_tabPressed(self): 
        pass

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
