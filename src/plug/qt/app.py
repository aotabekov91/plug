from PyQt5 import QtWidgets

from gizmo.ui import StackWindow

from plug.qt.plug import Plug

class PlugApp(Plug):

    def __init__(self, *args, argv=[], **kwargs):

        self.app=QtWidgets.QApplication([])

        super(PlugApp, self).__init__(
                *args,
                app=self.app,
                **kwargs,
                )

    def setGUI(self, 
               display_class=None, 
               view_class=None):

        self.window=StackWindow(
                self, 
                display_class, 
                view_class)


