from plug.qt import Plug

class Render(Plug):

    def initialize(self):

        d=getattr(self.app, 'display', None)
        if d: d.addViewer(self)
        b=getattr(self.app, 'buffer', None)
        if b: b.addModeller(self)

    def readModel(self, model):
        pass

    def readFile(self, path):
        pass

    def setId(self, path, model):
        pass

    def getView(self, model):
        return self.readModel(model)

    def getModel(self, path):

        m=self.readFile(path)
        if m: 
            self.setId(path, m)
        return m
