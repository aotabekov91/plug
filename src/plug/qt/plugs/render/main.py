from plug.qt import Plug

class Render(Plug):

    view_class=None
    model_class=None

    def initiate(self, *args, **kwargs):

        super().initiate(*args, **kwargs)
        self.app.addRender(self)

    def open(self, source=None, **kwargs):

        model=self.getModel(
                source, **kwargs)
        view=self.getView(
                model, **kwargs)
        self.setView(
                view, **kwargs)

    def getModel(self, source, **kwargs):

        if source and self.model_class:
            return self.model_class(
                    source=source)

    def getView(self, model, **kwargs):

        if model and self.view_class:
            return self.view_class(
                    model=model)

    def isCompatible(self, source):

        return self.model_class.isCompatible(
                source)

    def setView(self, view, **kwargs):
        pass
