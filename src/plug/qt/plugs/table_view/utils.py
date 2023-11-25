from gizmo.utils import tag
from gizmo.vimo.model import WTableModel
from gizmo.vimo.view import ListWidgetView

class TView(ListWidgetView):

    @classmethod
    def isCompatible(cls, m, **kwargs):
        return m and m.source()==cls.pattern

    @tag('t', modes=['command'])
    def toggle(self):
        super().toggle()

    @tag('o', modes=['|^own'])
    def open(self):

        i=self.currentItem()
        v=self.app.handler.type()
        if i and v:
            k=self.locator_kind
            d=i.element().data()
            v.openLocator(d, k)

    @tag('d', modes=['|^own'])
    def delete(self):

        i=self.currentItem()
        m=self.model()
        if i and m:
            e=i.element()
            m.removeElement(e)

class TModel(WTableModel):

    wantUniqView=True

    def __eq__(self, m):

        if not m: return False
        c1=m.name==self.name
        c2=m.source()==self.source()
        return c1 and c2

    @classmethod
    def isCompatible(cls, s, **kwargs):
        return s and s==cls.pattern

    @classmethod
    def getSourceName(
            cls, 
            source, 
            name=None,
            index=None, 
            **kwargs):

        return (index, name, source)
