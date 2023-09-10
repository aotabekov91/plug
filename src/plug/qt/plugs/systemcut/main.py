from plug import Plug
from PyQt5 import QtCore
from plug.qt.utils import KeyListener

class Systemcut(Plug, QtCore.QObject):

    def setSystemListener(self):

        self.os_thread = QtCore.QThread()
        self.os_listener=KeyListener(self)
        self.os_listener.moveToThread(self.os_thread)
        self.os_thread.started.connect(
                self.os_listener.loop)
        QtCore.QTimer.singleShot(0, self.os_thread.start)

