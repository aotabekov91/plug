import sys
from PyQt5 import QtWidgets

from gizmo.ui import StackWindow

from .base import Plug

class PlugApp(Plug, QtWidgets.QApplication):

    def __init__(self, 
                 initiate_stack=False, 
                 argv=[],
                 **kwargs):

        super(PlugApp, self).__init__(argv=argv, **kwargs)

    def setGUI(self, display_class=None, view_class=None):

        self.stack=StackWindow(
                self, 
                display_class, 
                view_class)

    def parse(self): 

        return self.parser.parse_known_args()

    def setName(self):

        super().setName()
        self.setApplicationName(self.name)

    def run(self):

        self.parse()
        self.running=True
        if hasattr(self, 'stack'): self.stack.show()
        sys.exit(self.exec_())

    def exit(self): 

        self.running=False
        sys.exit()
