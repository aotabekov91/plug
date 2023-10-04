from PyQt5 import QtCore
from plug.qt.plugs.connect import Connect
from plug.plugs.umay_plug import Umay as Base

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
