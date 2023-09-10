from PyQt5 import QtCore
from plug.qt.plugs.connect import Connect
from plug.plugs.handler import Handler as Base

class Handler(Base, QtCore.QObject):

    def setConnection(self):

        super().setConnection(connect=Connect)
