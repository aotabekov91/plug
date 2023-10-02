from PyQt5 import QtCore
from plug.plugs.umay import Umay as Base
from plug.qt.plugs.connect import Connect

class Umay(Base, QtCore.QObject):

    def setConnect(
            self, 
            port=None,
            connect=None,
            parent_port=None,
            **kwargs,
            ):

        super().setConnect(
                port=port,
                connect=Connect,
                parent_port=parent_port,
                **kwargs)
