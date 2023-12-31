from gizmo.utils import tag
from gizmo.vimo import view
from gizmo.vimo import model

from . import mixin

class View(
        mixin.Copy,
        view.mixin.TFullscreen,
        view.WListWidgetView
        ):

    def open(self):

        i=self.currentItem()
        v=self.app.handler.type()
        if i and v:
            k=self.locator_kind
            d=i.element().data()
            v.openLocator(d, k, view=v)

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

    @classmethod
    def getSourceName(
            cls, 
            source, 
            name=None,
            index=None, 
            **kwargs):

        return (index, name, source)


class TModel(Model, model.STableModel):
    pass

class RModel(Model, model.RTableModel):
    pass

class TView(view.Tabber):

    row_map={}
    widget_map={}
    canFollow=True
    tab_class=View

    def setup(self):

        super().setup()
        self.tab_class.widget_map=self.widget_map

    @tag('o', modes=['normal|^own'])
    def open(self):
        if self.current_tab:
            self.current_tab.open()

    @tag('d', modes=['normal|^own'])
    def delete(self):

        if self.current_tab:
            self.current_tab.delete()

    @tag('t', modes=['command'])
    def toggle(self):

        t=self.current_tab
        if t and t.isVisible():
            self.octivate()
        else:
            self.activate()

    @classmethod
    def isCompatible(cls, m, **kwargs):
        return cls.pattern==m.pattern

    def setModel(self, model):

        if not self.current_tab:
            self.tabAddNew()
        self.m_model=model
        self.current_tab.setModel(model)
