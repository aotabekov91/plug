import re
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

    def open(self, source=None, **kwargs):

        model=self.getModel(
                source, **kwargs)
        view=self.getView(
                model, **kwargs)
        self.setView(
                view, **kwargs)

    def getModel(self, source, **kwargs):

        if source:
            return self.model_class(
                    source=source)

    def getView(self, model, **kwargs):

        if model:
            return self.view_class(
                    model=model)

    def isCompatible(self, source):

        return self.model_class.isCompatible(
                source)

    def setView(self, view, **kwargs):
        pass
