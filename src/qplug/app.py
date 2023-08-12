import sys

from PyQt5 import QtWidgets

from .base import Plug
from ..core.ui import StackWindow
from ..core.manager import Manager

class PlugApp(Plug, QtWidgets.QApplication):

    def __init__(self, 
                 initiate_stack=False, 
                 argv=[],
                 **kwargs):

        super(PlugApp, self).__init__(argv=argv, **kwargs)
        if initiate_stack: self.initiate()

    def initiate(self):

        self.setManager()
        self.setStack()

        self.loadPlugs()
        self.loadModes()

        self.parse()

    def setStack(self, 
                 display_class=None, 
                 view_class=None):

        self.stack=StackWindow(
                self, 
                display_class, 
                view_class)

    def setManager(self, 
                   manager=None, 
                   buffer=None, 
                   plug=None, 
                   mode=None):

        if not manager: manager=Manager
        self.manager=manager(self, buffer, mode, plug)

    def loadModes(self): 

        if hasattr(self, 'modes'): self.modes.load()

    def loadPlugs(self): 

        if hasattr(self, 'plugs'): self.plugs.load()

    def parse(self): 

        return self.parser.parse_known_args()

    def setName(self):

        super().setName()
        self.setApplicationName(self.name)

    def run(self):

        self.running=True
        if hasattr(self, 'stack'): self.stack.show()
        sys.exit(self.exec_())

    def exit(self): 

        self.running=False
        sys.exit()
