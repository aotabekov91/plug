from PyQt5 import QtCore
from plug.plugs.umay import Umay as Base
from plug.qt.plugs.connect import Connect

class Umay(Base, QtCore.QObject):

    def setConnection(self):

        super().setConnection(connect=Connect)
