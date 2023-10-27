from plug.qt import Plug

class Render(Plug):

    def initiate(
            self, 
            view=None, 
            model=None
            ):

        super().initiate()
        self.view_class=view
        self.model_class=model
        b=getattr(self.app, 'buffer', None)
        d=getattr(self.app, 'display', None)
        if d: d.addViewer(self)
        if b: b.addModeller(self)

    def setId(self, source, model):

        if model:
            model.setId(id(model))

    def getModel(self, source):

        model=self.readSource(source)
        self.setId(source, model)
        return model

    def getView(self, model):
        return None

    def readSource(self, source):
        return None
