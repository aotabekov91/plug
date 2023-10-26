from plug.qt import Plug
from gizmo.utils import register

from .widget import PowerlineWidget

class Powerline(Plug):

    def __init__(
            self, 
            prefix_keys={'command': 'P'}, 
            **kwargs
            ):

        super().__init__(
                prefix_keys=prefix_keys,
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

        if name: name=name.title()
        self.ui.setText('detail', name) 

    def on_keysChanged(self, keys):
        self.ui.setText('keys', keys)

    def on_modeChanged(self, mode):

        name=None
        if mode: name=mode.name.title()
        self.ui.setText('mode', name) 

    def on_viewChanged(self, view, prev): 

        uid=''
        if view: uid=view.model().id()
        self.ui.setText('model', uid)
        self.on_itemChanged(view)

    def on_itemChanged(self, view, item=None): 

        page=''
        if view:
            cpage=view.current()
            tpages=view.count()
            page=f'{cpage}/{tpages}'
        self.ui.setText('page', page)
