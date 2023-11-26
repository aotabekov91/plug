from plug.qt import Plug
from gizmo.utils import tag

from .widget import PowerlineWidget

class Powerline(Plug):

    view=None
    prefix_keys={'command': 'P'}

    def setup(self):

        super().setup()
        self.app.earman.keysChanged.connect(
                self.setKeys)
        self.app.handler.modeChanged.connect(
                self.setMode)
        self.app.handler.submodeChanged.connect(
                self.setSubmode)
        self.app.handler.typeChanged.connect(
                self.updateType)
        self.app.handler.viewChanged.connect(
                self.updateView)
        self.bar=self.app.ui.bar
        self.setupUI()

    def updateType(self, v):

        if v:
            self.setKind(v)
            self.setModel(v.model())

    def updateView(self, v):

        self.reconnect()
        self.view=v
        self.setView(v)
        self.reconnect('connect')

    def reconnect(self, kind='disconnect'):

        if self.view:
            for f in ['indexChanged',]:
                s=getattr(self.view, f, None)
                if s:
                    s=getattr(s, kind)
                    s(getattr(self, 'setIndex'))

    def setupUI(self):

        self.ui=PowerlineWidget()
        self.bar.clayout.insertWidget(0, self.ui)
        self.bar.show()

    def setMode(self, m=None):

        if m: m=m.name.title()
        self.ui.setText('mode', m) 

    def setSubmode(self, s=None):

        if s: s=s.name.title()
        self.ui.setText('submode', s) 

    def setModel(self, model=None): 

        if model: 
            model=model.id()
        self.ui.setText('model', model)

    def setDetail(self, name):

        if name: name=name.title()
        self.ui.setText('detail', name) 

    def setKeys(self, keys=None):
        self.ui.setText('keys', keys)

    def setKind(self, view=None):

        if view: 
            k=view.kind
            if k: view=k.title()
        self.ui.setText('type', view)

    def setView(self, view=None): 

        if view:
            idx=None
            if hasattr(view, 'currentIndex'):
                c=view.currentIndex()
                if type(c)==int: idx=c
            self.setIndex(idx)
            view=view.name
        self.ui.setText('view', view)

    def setIndex(self, idx=None): 

        if idx and hasattr(self.view, 'count'):
            idx=f'{idx}/{self.view.count()}'
        self.ui.setText('index', idx)
