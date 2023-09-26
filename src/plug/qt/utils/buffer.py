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
        self.watch.fileChanged.connect(
                self.on_fileChanged)

    def addModeller(self, modeller):
        self.modellers+=[modeller]

    def getModel(self, path):

        for m in self.modellers:
            return m.getModel(path)

    def load(self, path):

        path=os.path.abspath(path)
        if path in self.buffers:
            return self.buffers[path]
        model=self.getModel(path)
        if model and model.readSuccess():
            self.setID(path, model)
            self.buffers[path]=model
            self.bufferCreated.emit(model)
            return model

    def setID(self, path, model):
        pass

    def on_fileChanged(self, path): 
        pass

    def watchFile(self, path): 

        self.watch.addPath(
                os.path.realpath(path))
