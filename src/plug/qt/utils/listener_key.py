from PyQt5 import QtCore
from plug.utils.listener_key import KeyListener as BaseListener

class KeyListener(BaseListener, QtCore.QObject): pass
