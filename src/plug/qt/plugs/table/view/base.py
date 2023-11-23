from gizmo.utils import tag
from plug.qt.plugs.render import Render
from gizmo.vimo.model import WTableModel
from gizmo.vimo.view import ListWidgetView

class TableView(Render):

    kind=None
    table=None
    widget_map={}
    leader_keys={}
    view_prop='canLocate'
    locator_kind='position'
    model_class=WTableModel
    view_class=ListWidgetView

    def setup(self):

        super().setup()
        self.rendering=False
        self.m_view=self.view_class(
                render=self, 
                kind=self.kind,
                name=self.view_name)
        self.app.moder.typeChanged.connect(
                self.setType)
        self.app.uiman.setupUI(
                self, 
                self.m_view, 
                self.view_name)

    def getModel(self, view):

        uid=view.getUniqLocator()
        uid['type']=self.kind
        b=self.app.buffer
        m=b.getModel(uid)
        if m is None: 
            uid=view.getUniqLocator()
            m=self.model_class(
                    index=uid, 
                    kind=self.kind,
                    table=self.table,
                    widget_map=self.widget_map)
            uid['type']=self.kind
            b.setModel(uid, m)
            m.load()
        return m

    def setType(self, t):

        v=self.checkView(t)
        if v:
            m=self.getModel(v)
            self.m_view.setModel(m)

    def checkView(self, t=None):

        t = t or self.app.moder.type()
        v=t.view()
        if v and v.check(self.view_prop):
            return v

    def open(self):

        i=self.m_view.currentItem()
        t=self.app.moder.type()
        v=t.view()
        if i and v:
            k=self.locator_kind
            d=i.element().data()
            v.openLocator(d, k)

    def delete(self):

        t=self.app.moder.type()
        m=self.getModel(t.view())
        i=self.m_view.currentItem()
        if i and m:
            e=i.element()
            m.removeElement(e)

    def toggleRender(self):

        if self.rendering:
            self.rendering=False
            self.app.uiman.deactivate(
                    self, self.m_view)
        else:
            self.rendering=True
            self.setCurrentView(self.m_view)
