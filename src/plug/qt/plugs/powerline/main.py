from plug.qt import Plug
from gizmo.utils import tag

from .widget import PowerlineWidget

class Powerline(Plug):

    view=None
    leader_keys={'command': 'P'}

    def setup(self):

        super().setup()
        self.app.earman.keysChanged.connect(
                self.setKeys)
        self.app.moder.modeChanged.connect(
                self.setMode)
        self.app.moder.typeChanged.connect(
                self.updateType)
        self.app.moder.viewChanged.connect(
                self.updateView)
        self.bar=self.app.window.bar
        self.setUI()

    def updateType(self, t):

        if t:
            self.setType(t)
            model=None
            if t.view: model=t.view.model()
            self.setModel(model)

    def updateView(self, view):

        self.reconnect()
        self.view=view
        self.setView(view)
        self.reconnect('connect')

    def reconnect(self, kind='disconnect'):

        if self.view:
            for f in ['indexChanged',]:
                s=getattr(self.view, f, None)
                if s:
                    s=getattr(s, kind)
                    s(getattr(self, 'setIndex'))

    def setUI(self):

        self.ui=PowerlineWidget()
        self.bar.clayout.insertWidget(0, self.ui)
        self.bar.show()

    def setMode(self, mode=None):

        if mode: 
            mode=mode.name.title()
        self.ui.setText('mode', mode) 

    def setModel(self, model=None): 

        if model: 
            model=model.id()
        self.ui.setText('model', model)

    def setDetail(self, name):

        if name: 
            name=name.title()
        self.ui.setText('detail', name) 

    def setKeys(self, keys=None):
        self.ui.setText('keys', keys)

    def setType(self, pype=None):

        if pype: 
            pype=pype.type().title()
        self.ui.setText('type', pype)

    def setView(self, view=None): 

        if view:
            view=view.__class__.__name__
            if hasattr(view, 'name'):
                view=view.name()
        self.ui.setText('view', view)

    def setIndex(self, idx=None): 

        if idx and hasattr(self.view, 'count'):
            idx=f'{idx}/{self.view.count()}'
        self.ui.setText('index', idx)
