import re
import shlex
from PyQt5 import QtCore
from inspect import signature, Parameter

from plug.qt import Plug
from plug.plugs.parser import Parser

class Exec(Plug):

    name='run'
    functions={}
    listen_leader='<c-e>'

    def event_functor(self, e, ear):

        enter=[
               QtCore.Qt.Key_Enter,
               QtCore.Qt.Key_Return, 
              ]
        if e.key() in enter:
            self.execute()
            self.octivate()
            return True

    def setup(self):

        super().setup()
        self.setParser()
        self.bar=self.app.ui.bar
        self.app.earman.objectAdded.connect(
                self.setModeFunctions)

    def setParser(self):

        self.parser=Parser()
        self.parser.addArgument('exec')

    def setModeFunctions(self, plugs):

        m=self.app.earman.m_methods
        funcs=m.get('exec', [])
        for f in funcs:
            n=f.__name__
            self.functions[n]=f

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

    def activate(self):

        super().activate()
        self.activateBar()

    def octivate(self):

        super().octivate()
        self.octivateBar()

    def octivateBar(self):

        self.bar.bottom.hide()
        self.bar.edit.clear()

    def activateBar(self):

        self.bar.bottom.show()
        self.bar.show()
        self.bar.edit.setFocus()

    def updateKeysSet(self, commands):

        # self.app.earman.plugsLoaded.connect(
                # self.updateKeysSet) # todo

        f=self.app.earman.commands.get(
                self, {})
        default=f.get('default', {})
        for c, m in default.items():
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

    def execute(self): 

        f, a=self.getMethodByName()
        print(f, a)

    def getMethodByName(self):

        t=self.app.ui.bar.edit.text()
        c, u = self.parser.parse(t)
        print(c, u)
        if c.exec:
            m, p = [], []
            for n, f in self.functions.items():
                if n==c.exec:
                    m+=[f]
                elif n[0:len(c.exec)]==c.exec:
                    p+=[f]
        print(m, p, c.exec, u)
        u=vars(u)
        raise
