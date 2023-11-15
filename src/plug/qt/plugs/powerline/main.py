from plug.qt import Plug
from gizmo.utils import tag

from .widget import PowerlineWidget

class Powerline(Plug):

    view=None
    mode=None
    leader_keys={'command': 'P'}

    def setup(self):

        super().setup()
        self.app.earman.keysChanged.connect(
                self.on_keysChanged)
        self.app.moder.modeChanged.connect(
                self.updateMode)
        self.bar=self.app.window.bar
        self.setUI()

    def updateMode(self, m):

        if m:
            self.reconnect()
            self.mode=m
            self.setMode(m)
            self.view=None
            if self.checkProp('hasView', m):
                self.view=m.getView()
                self.setView(self.view)
            self.reconnect('connect')

    def reconnect(self, kind='disconnect'):

        if self.mode:
            for f in ['detailChanged']:
                s=getattr(self.mode, f, None)
                if s:
                    s=getattr(s, kind)
                    s(getattr(self, f'on_{f}'))
        if self.view:
            for f in ['indexChanged',]:
                s=getattr(self.view, f, None)
                if s:
                    s=getattr(s, kind)
                    s(getattr(self, f'on_{f}'))

    def setUI(self):

        self.ui=PowerlineWidget()
        self.bar.clayout.insertWidget(
                0, self.ui)
        self.bar.show()

    def setMode(self, mode):

        name=None
        if mode: 
            name=mode.name.title()
        self.ui.setText('mode', name) 

    def setView(self, curr): 

        uid=None
        if curr: 
            uid=curr.model().id()
        self.ui.setText('model', uid)

    def on_detailChanged(self, name):

        if name: 
            name=name.title()
        self.ui.setText('detail', name) 

    def on_keysChanged(self, keys):
        self.ui.setText('keys', keys)

    def on_indexChanged(self, idx): 

        idx=f'{idx}/{self.view.count()}'
        self.ui.setText('page', idx)
