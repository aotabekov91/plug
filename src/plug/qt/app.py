import sys
from PyQt5 import QtWidgets

from gizmo.ui import StackWindow

from .base import Plug
from .utils import Plugman

class PlugApp(Plug, QtWidgets.QApplication):

    def __init__(self, argv=[], **kwargs):

        super(PlugApp, self).__init__(
                argv=argv, 
                **kwargs)

        if self.css_style:
            self.setStyleSheet(self.css_style)

    def setGUI(self, 
               display_class=None, 
               view_class=None):

        self.window=StackWindow(
                self, 
                display_class, 
                view_class)

    def setPlugman(self): 
        self.plugman=Plugman(self)

    def parse(self): 
        return self.parser.parse_known_args()

    def setName(self):

        super().setName()
        self.setApplicationName(self.name)

    def run(self):

        if hasattr(self, 'parser'):
            self.parse()
        self.running=True
        if hasattr(self, 'window'): self.window.show()
        sys.exit(self.exec_())

    def exit(self): 

        self.running=False
        sys.exit()
