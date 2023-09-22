from plug.qt import Plug
from gizmo.utils import register

from .widget import PowerlineWidget

class Powerline(Plug):

    def __init__(self, 
                 prefix_key={'command': 'l'},
                 **kwargs):

        super().__init__(
                prefix_key=prefix_key,
                **kwargs)
        self.app.plugman.modeChanged.connect(
                self.on_modeChanged)
        self.app.plugman.keysChanged.connect(
                self.on_keysChanged)
        self.app.window.main.display.itemChanged.connect(
                self.on_itemChanged)
        self.app.window.main.display.viewChanged.connect(
                self.on_viewChanged)
        if hasattr(self.app, 'buffer'):
            self.app.buffer.hashChanged.connect(
                    self.on_hashChanged)
        self.setUI()
        self.activate()

    def on_keysChanged(self, pressed):

        if pressed:
            self.ui.setText('keys', pressed)

    def on_modeChanged(self, mode):

        if mode:
            self.ui.setText(
                    'mode', mode.name.title())

    def setUI(self):

        self.ui=PowerlineWidget()
        self.app.window.bar.container_layout.insertWidget(
                0, self.ui)
        self.app.window.bar.show()

    def on_hashChanged(self, model):

        if model:
            dhash=model.hash()
            if dhash: 
                self.ui.setText('model', dhash)

    def on_viewChanged(self, view, prev): 

        name=view.model().hash()
        if name:
            self.ui.setText('model', name)
        self.on_itemChanged(view)

    def on_itemChanged(self, view, item=None): 

        cpage=view.currentPage()
        pages=view.totalPages()
        if pages:
            self.ui.setText(
                    'page', f'{cpage}/{pages}')

    @register('t', modes=['command'])
    def toggle(self): super().toggle()
