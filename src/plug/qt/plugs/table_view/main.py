import tables
from plug.qt import Plug
from gizmo.utils import tag
from gizmo.vimo import view
from functools import partial

from .utils import TModel, RModel, TView

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
        RModel.pattern=self.pattern
        self.app.handler.addViewer(TView)
        self.app.handler.addModeller(TModel)
        self.app.handler.addModeller(RModel)

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
        if not v.model(): return
        if not v.check('canLocate'): return
        for k, c in self.config.items():
            exc = ['General', 'Settings']
            if k in exc: continue
            uid=v.getUniqLocator()
            f=self.app.handler.handleInitiate
            name=c.get('name')
            ff=f(
             config=c, 
             index=uid,
             name=name, 
             source=self.pattern,
             )
