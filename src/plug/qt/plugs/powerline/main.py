from plug.qt import Plug
from gizmo.utils import register

from .widget import PowerlineWidget

class Powerline(Plug):

    def __init__(
            self, 
            leader_keys={'command': 'P'}, 
            **kwargs
            ):

        super().__init__(
                leader_keys=leader_keys,
                **kwargs)
        self.setUI()
        self.app.moder.modeChanged.connect(
                self.on_modeChanged)
        self.app.moder.keysChanged.connect(
                self.on_keysChanged)
        self.app.moder.detailChanged.connect(
                self.on_detailChanged)
        self.app.display.itemChanged.connect(
                self.on_itemChanged)
        self.app.display.viewChanged.connect(
                self.on_viewChanged)
        self.activate()

    def setUI(self):

        self.ui=PowerlineWidget()
        bar=self.app.window.bar
        bar.clayout.insertWidget(
                0, self.ui)
        self.app.window.bar.show()

    def on_detailChanged(self, name):

        if name: 
            name=name.title()
        self.ui.setText('detail', name) 

    def on_keysChanged(self, keys):
        self.ui.setText('keys', keys)

    def on_modeChanged(self, mode):

        name=None
        if mode: 
            name=mode.name.title()
        self.ui.setText('mode', name) 

    def on_viewChanged(self, view, prev): 

        uid=None
        if view: 
            uid=view.model().id()
        self.ui.setText('model', uid)

    def on_itemChanged(self, view, item): 

        page=None
        if view and item:
            t=view.count()
            c=item.index()
            page=f'{c}/{t}'
        self.ui.setText('page', page)
