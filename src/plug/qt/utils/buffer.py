from PyQt5 import QtCore

class Buffer(QtCore.QObject):

    bufferCreated=QtCore.pyqtSignal(object)

    def __init__(self, app):

        self.buffers={}
        super().__init__(app)

    def get(self, idx):

        if idx in self.buffers:
            return self.buffers[idx]

    def set(self, idx, buffer):

        if buffer: 
            self.buffers[idx]=buffer
            self.bufferCreated.emit(buffer)
