from plug.qt import Plug
from gizmo.utils import register

from .widget import PowerlineWidget

class Powerline(Plug):

    def __init__(
            self, 
            leader_keys={'command': 'P'}, 
            **kwargs
            ):

        self.view=None
        self.mode=None
        super().__init__(
                leader_keys=leader_keys,
                **kwargs)
        self.app.moder.modeChanged.connect(
                self.updateMode)
        self.setUI()

    def updateMode(self, mode):

        if mode:
            self.resetMode()
            self.mode=mode
            self.view=mode.getView()
            self.resetMode('connect')
            self.setMode(mode)
            self.setView(self.view)

    def resetMode(self, kind='disconnect'):

        if self.mode:
            for f in ['keysChanged', 'detailChanged']:
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
        bar=self.app.window.bar
        bar.clayout.insertWidget(
                0, self.ui)
        self.app.window.bar.show()
        self.uiman.activate()

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
