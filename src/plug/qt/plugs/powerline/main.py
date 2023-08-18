from plug.qt import PlugObj

from .widget import StatusWidget

class Powerline(PlugObj):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.app.plugman.modeChanged.connect(self.on_modeChanged)
        self.app.main.display.viewChanged.connect(self.on_viewChanged)

        self.setUI()

    def on_modeChanged(self, mode):

        self.ui.mode.setText(mode.name)

    def setUI(self):

        self.ui=StatusWidget()
        self.app.main.main_layout.addWidget(self.ui)

    def on_viewChanged(self, view): 

        self.on_itemChanged(view) 

    def on_itemChanged(self, view, item=None): 

        cpage=view.currentPage()
        pages=view.totalPages()
        self.ui.page.setText(f'{cpage}/{pages}')
