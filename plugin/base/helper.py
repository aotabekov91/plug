from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

def key(key):
    def _key(func):
        def inner(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        inner.key=key
        return inner
    return _key

class ZMQListener(QObject):

    request = pyqtSignal(dict)

    def __init__(self, parent):
        super(ZMQListener, self).__init__()
        self.parent = parent

    def loop(self):
        while self.parent.activated:
            request = self.parent.socket.recv_json()
            self.request.emit(request)
