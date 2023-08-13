import os

from PyQt5 import QtCore

class Buffman(QtCore.QObject):

    bufferCreated=QtCore.pyqtSignal(object)

    def __init__(self, app):

        super().__init__()

        self.app=app
        self.buffers={}

        self.watch=QtCore.QFileSystemWatcher()
        self.watch.fileChanged.connect(self.on_fileChanged)

    def load(self, filePath): pass 

    def on_fileChanged(self, filePath): pass

    def watchFile(self, filePath): 

        self.watch.addPath(os.path.realpath(filePath))
