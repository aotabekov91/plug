from plug.qt import Plug
from gizmo.utils import register

from .widget import PowerlineWidget

class Powerline(Plug):

    def __init__(self, 
                 prefix_keys={'command': 'l'},
                 **kwargs):

        super().__init__(
                prefix_keys=prefix_keys,
                **kwargs)
        self.app.moder.modeChanged.connect(
                self.on_modeChanged)
        self.app.moder.keysChanged.connect(
                self.on_keysChanged)
        self.app.display.itemChanged.connect(
                self.on_itemChanged)
        self.app.display.viewChanged.connect(
                self.on_viewChanged)

        self.activate()

    def setup(self):

        super().setup()
        self.setUI()

    def on_keysChanged(self, keys):

        if keys:
            self.ui.setText('keys', keys)

    def on_modeChanged(self, mode):

        if mode:
            self.ui.setText(
                    'mode', 
                    mode.name.title()
                    )

    def setUI(self):

        self.ui=PowerlineWidget()
        bar=self.app.window.bar
        bar.container_layout.insertWidget(
                0, self.ui)
        self.app.window.bar.show()

    def on_viewChanged(self, view, prev): 

        uid=''
        if view:
            uid=view.model().id()
        self.ui.setText('model', uid)
        self.on_itemChanged(view)

    def on_itemChanged(self, view, item=None): 

        page=''
        if view:
            cpage=view.currentPage()
            tpages=view.totalPages()
            page=f'{cpage}/{tpages}'
        self.ui.setText('page', page)

    @register('t', modes=['command'])
    def toggle(self): super().toggle()
