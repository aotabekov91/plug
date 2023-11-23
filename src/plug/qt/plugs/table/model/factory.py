import tables
from plug.qt import Plug
from PyQt5 import QtCore
from gizmo.vimo.model import WTableModel
from gizmo.vimo.view import ListWidgetView

class TableModelFactory(QtCore.QObject):

    model_class=WTableModel
    view_class=ListWidgetView

    def setTable(self):

        raise
        tclass=getattr(
                tables, 
                self.table_name,
                None)

    def createFactories(self):

        self.m_factories={}
        print(self.config)
        for k, v in self.config.items():
            if type(v)==dict:
                print(k, v)

    def setup(self):

        super().setup()
        self.createFactories()
        # self.app.moder.typeChanged.connect(
        #         self.checkModel)

    def getModel(self, v):

        uid=v.getUniqLocator()
        uid['type']=self.kind
        b=self.app.buffer
        m=b.getModel(uid)
        if m is None: 
            uid=v.getUniqLocator()
            m=self.model_class(
                    index=uid, 
                    kind=self.kind,
                    table=self.table,
                    widget_map=self.widget_map)
            uid['type']=self.kind
            b.setModel(uid, m)
            m.load()
        return m

    def checkModel(self, t=None):

        t = t or self.app.moder.type()
        if t.view(): self.getModel(t.view())
