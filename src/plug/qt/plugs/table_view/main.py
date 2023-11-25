from plug.qt import Plug

from .utils import TView, TModel

class TableView(Plug):

    def setup(self):

        super().setup()
        self.setClasses()
        self.updateSetup()
        self.app.handler.viewChanged.connect(
                self.updateView)

    def setClasses(self):

        TView.pattern=self.pattern
        TModel.pattern=self.pattern
        self.app.handler.addViewer(TView)
        self.app.handler.addModeller(TModel)

    def updateSetup(self):

        g=self.config.get('General', {})
        for k, y in self.config.items():
            if k!='General':
                c=g.copy()
                c.update(y)
                self.config[k]=c

    def updateView(self, v):

        if not v: return
        if not v.model().isType: return
        for k, d in self.config.items():
            exc = ['General', 'Settings']
            if k in exc: continue
            self.app.handler.handleInitiate(
                    setup=d, 
                    name=d.get('table'),
                    source=self.pattern, 
                    index=v.getUniqLocator())
