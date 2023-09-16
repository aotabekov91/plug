import sys
from PyQt5 import QtWidgets

from gizmo.ui import StackWindow

from .base import Plug
from .utils import Plugman

class PlugApp(Plug, QtWidgets.QApplication):

    def __init__(self, *args, argv=[], **kwargs):

        super(QtWidgets.QApplication).__init__(argv=argv)
        super(PlugApp, self).__init__(*args, **kwargs)

    def setGUI(self, 
               display_class=None, 
               view_class=None):

        self.window=StackWindow(
                self, 
                display_class, 
                view_class)

    def setup(self):

        super().setup()
        self.setPlugman(plugman=Plugman)

    def initialize(self):

        self.plugman.loadPicks()

    def setName(self):

        super().setName()
        self.setApplicationName(self.name)

    def run(self):

        super().run()
        if hasattr(self, 'window'): 
            self.window.show()
        sys.exit(self.exec_())

    def exit(self): 

        super().exit()
        sys.exit()
