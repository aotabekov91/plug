from PyQt5 import QtCore
from plug.qt.plugs.connect import Connect
from plug.plugs.handler import Handler as Base

class Handler(Base, QtCore.QObject):

    def setup(self):

        self.app=self.kwargs.get('app', self)
        self.setConnection()
        super().setup()

    def setConnection(self):

        if self.app:
            port=getattr(
                    self.app, 
                    'handler_port', 
                    None)
            if port: 
                self.port=port

    def setConnect(
            self, port, connect=Connect):

        if port:
            self.connect=Connect(
                    port=port,
                    app=self.app,
                    handler=self.handle
                    )
            self.run()
