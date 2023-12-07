from gizmo.utils import tag
from gizmo.vimo.view import ListWidgetView, Tabber
from gizmo.vimo.model import STableModel, RTableModel

from . import mixin

class View(
        mixin.Copy,
        ListWidgetView
        ):

    canFollow=True

    @tag('o', modes=['|^own'])
    def open(self):

        i=self.currentItem()
        v=self.app.handler.type()
        if i and v:
            k=self.locator_kind
            d=i.element().data()
            v.openLocator(d, k, view=v)

    @tag('d', modes=['|^own'])
    def delete(self):

        i=self.currentItem()
        m=self.model()
        if i and m:
            e=i.element()
            m.removeElement(e)

class Model:

    def __eq__(self, m):

        if not m: return False
        c1=m.name==self.name
        c2=m.source()==self.source()
        c3=m.id()==self.id()
        return c1 and c2 and c3

    @classmethod
    def isCompatible(cls, source, **kwargs):
        return source==cls.pattern

class TModel(Model, WTableModel):
    pass

class RModel(Model, RTableModel):
    pass

class TView(Tabber):

    row_map={}
    widget_map={}
    canFollow=True
    tab_class=View

    def setup(self):

        super().setup()
        print(self.name)
        print(self.widget_map)

    @classmethod
    def isCompatible(cls, m, **kwargs):
        return cls.pattern==m.pattern

    def setModel(self, model):

        if not self.current_tab:
            self.tabAddNew()
        self.m_model=model
        self.current_tab.setModel(model)
