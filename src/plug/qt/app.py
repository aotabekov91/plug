from PyQt5 import QtWidgets

from gizmo.ui import StackWindow

from plug.qt.plug import Plug

class PlugApp(Plug):

    def __init__(self, *args, argv=[], **kwargs):

        self.qapp=QtWidgets.QApplication([])

        super(PlugApp, self).__init__(
                *args,
                qapp=self.qapp,
                **kwargs,
                )

    def setGUI(self, 
               display_class=None, 
               view_class=None):

        self.window=StackWindow(
                self, 
                display_class, 
                view_class)


