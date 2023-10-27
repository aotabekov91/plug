from plug.qt import Plug

class Render(Plug):

    def initiate(
            self, 
            view_class=None, 
            model_class=None,
            ):

        super().initiate()
        self.view_class=view_class
        self.model_class=model_class
        self.app.addRender(self)

    def setId(self, source, model):

        if model:
            model.setId(id(model))

    def getModel(self, source):

        model=self.readSource(source)
        self.setId(source, model)
        return model

    def getView(self, model, **kwargs):

        if model:
            source=model.source()
            if self.isCompatible(source):
                view=self.view_class(
                        self.app, **kwargs)
                view.setModel(model)
                return view

    def readSource(self, source):

        if self.isCompatible(source):
            return self.model_class(
                    source=source)

    def isCompatible(self, source):
        return False
