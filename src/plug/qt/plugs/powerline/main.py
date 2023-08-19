from plug.qt import PlugObj
from plug.qt.utils import register

from .widget import StatusWidget

class Powerline(PlugObj):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

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
            self.ui.detail.show()
            self.ui.detail.setText(pressed)

    def on_modeChanged(self, mode):

        self.ui.mode.setText(mode.name.title())

    def setUI(self):

        self.ui=StatusWidget()
        self.app.window.bar.container_layout.insertWidget(
                0, self.ui)
        self.app.window.bar.show()

    def on_hashChanged(self, model):

        dhash=model.hash()
        if dhash:
            self.ui.model.show()
            self.ui.model.setText(dhash)

    def on_viewChanged(self, view): 

        name=view.name()
        if name:
            self.ui.model.show()
            self.ui.model.setText(name)

    def on_itemChanged(self, view, item=None): 

        cpage=view.currentPage()
        pages=view.totalPages()
        if pages:
            self.ui.page.show()
            self.ui.page.setText(f'{cpage}/{pages}')

    @register('t', modes=['command'])
    def toggle(self): super().toggle()
