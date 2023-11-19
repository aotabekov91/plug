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
                self.setKeys)
        self.app.moder.typeChanged.connect(
                self.setType)
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
                    s(getattr(self, 'setDetail'))
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

    def setMode(self, mode):

        name=None
        if mode: name=mode.name.title()
        self.ui.setText('mode', name) 

    def setView(self, curr): 

        uid=None
        if curr: 
            m=curr.model()
            if m: uid=curr.model().id()
        self.ui.setText('model', uid)

    def setDetail(self, name):

        if name: name=name.title()
        self.ui.setText('detail', name) 

    def setKeys(self, keys):
        self.ui.setText('keys', keys)

    def setType(self, view): 

        m=view.model()
        if m: m=f'[{m.kind.title()}]'
        self.ui.setText('submode', m)

    def setIndex(self, idx): 

        idx=f'{idx}/{self.view.count()}'
        self.ui.setText('index', idx)
