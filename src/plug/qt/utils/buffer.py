from PyQt5 import QtCore

class Buffer(QtCore.QObject):

    bufferCreated=QtCore.pyqtSignal(object)

    def __init__(self, app):

        super().__init__(app)
        self.app=app
        self.buffers={}

    def getModel(self, source):

        for agent in self.app.renders:
            m=agent.getModel(source)
            if m: return m

    def load(self, source):

        if source in self.buffers:
            return self.buffers[source]
        model=self.getModel(source)
        if model and model.readSuccess():
            self.buffers[source]=model
            self.bufferCreated.emit(model)
            return model
