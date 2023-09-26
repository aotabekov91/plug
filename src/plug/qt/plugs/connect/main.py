from PyQt5 import QtCore
from plug.qt.utils import ZMQListener
from plug.plugs.connect import Connect as Base

class Connect(Base, QtCore.QObject):

    def setup(self):

        super().setup()
        self.setListener()

    def run(self):

        self.running=True
        QtCore.QTimer.singleShot(
                0, self.listener.start)

    def setListener(self):

        self.zeromq=ZMQListener(self)
        self.listener = QtCore.QThread()
        self.zeromq.request.connect(
                self.handle)
        self.zeromq.moveToThread(
                self.listener)
        self.listener.started.connect(
                self.zeromq.loop)

    def handle(self, request):

        respond=super().handle(request)
        if respond: 
            self.socket.send_json(respond)
        self.zeromq.acted=True
