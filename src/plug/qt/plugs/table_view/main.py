import tables
from plug.qt import Plug

from .utils import TView, TModel

class TableView(Plug):

    def setup(self):

        super().setup()
        self.setClasses()
        self.updateConfs()
        self.app.handler.viewChanged.connect(
                self.updateView)

    def setClasses(self):

        TView.pattern=self.pattern
        TModel.pattern=self.pattern
        self.app.handler.addViewer(TView)
        self.app.handler.addModeller(TModel)

    def updateConfs(self):

        g=self.config.get('General', {})
        for k, y in self.config.items():
            if k!='General':
                c=g.copy()
                c.update(y)
                tn=c.get('table_name', '')
                tc=getattr(tables, tn, None)
                if tc: 
                    c['name']=tn
                    c['table']=tc()
                self.config[k]=c

    def updateView(self, v):

        if not v: return
        if not v.model().isType: return
        for k, c in self.config.items():
            exc = ['General', 'Settings']
            if k in exc: continue
            self.app.handler.handleInitiate(
                    config=c, 
                    name=c.get('name'),
                    source=self.pattern, 
                    index=v.getUniqLocator())
