from plug.qt import Plug

class Render(Plug):

    def initiate(self):

        super().initiate()
        display=getattr(
                self.app, 
                'display', 
                None)
        if display: 
            display.addViewer(self)
        buffer=getattr(
                self.app, 'buffer', None)
        if buffer: 
            buffer.addModeller(self)

    def getModel(self, path):

        model=self.readFile(path)
        if model: 
            self.setId(path, model)
        return model

    def setId(self, path, model):

        if model:
            model.setId(id(model))

    def getView(self, model):
        return self.readModel(model)

    def readModel(self, model):
        return

    def readFile(self, path):
        return
