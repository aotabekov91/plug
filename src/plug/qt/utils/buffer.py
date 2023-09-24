import os

from PyQt5 import QtCore

class Buffer(QtCore.QObject):

    bufferCreated=QtCore.pyqtSignal(object)

    def __init__(self, app):

        super().__init__(app)

        self.app=app
        self.buffers={}
        self.modellers=[]

        self.watch=QtCore.QFileSystemWatcher()
        self.watch.fileChanged.connect(self.on_fileChanged)

    def addModeller(self, modeller):
        self.modellers+=[modeller]

    def getModel(self, path):

        for m in self.modellers:
            model=m.getModel(path)
            if model: 
                return model

    def load(self, path):

        path=os.path.abspath(path)
        if path in self.buffers:
            return self.buffers[path]
        model=self.getModel(path)
        if model and model.readSuccess():
            self.buffers[path]=model
            self.setHash(path)
            self.bufferCreated.emit(model)
            return model

    def on_fileChanged(self, filePath): pass

    def watchFile(self, filePath): 

        self.watch.addPath(os.path.realpath(filePath))
