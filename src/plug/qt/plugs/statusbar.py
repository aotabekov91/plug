from PyQt5 import QtCore, QtWidgets

from ..configure import Configure
from ...utils import register

class StatusBar(QtWidgets.QStatusBar):

    hideWanted=QtCore.pyqtSignal()
    toggled=QtCore.pyqtSignal(bool)
    keyPressed=QtCore.pyqtSignal(object)

    def __init__(self, window):

        super(StatusBar, self).__init__()

        self.window=window
        self.configure=Configure(
                app=window.app, 
                parent=self)

        self.setUI()

        self.window.display.viewChanged.connect(
                self.on_viewChanged)

        self.window.display.itemChanged.connect(
                self.on_itemChanged)

        self.window.app.buffer.hashChanged.connect(
                self.on_hashChanged)

    def setUI(self):

        self.style_sheet='''
            QLineEdit {
                background-color: transparent;
                border-color: transparent;
                border-width: 0px;
                border-radius: 0px;
                }
            QLabel{
                background-color: transparent;
                }
                '''

        layout=self.layout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.mode=QtWidgets.QLabel()
        self.info=QtWidgets.QLabel()
        self.edit=QtWidgets.QLineEdit(self)
        self.detail=QtWidgets.QLabel()
        self.model=QtWidgets.QLabel()
        self.page=QtWidgets.QLabel()

        self.setFixedHeight(25)

        self.addPermanentWidget(self.mode, 1)
        self.addPermanentWidget(self.info, 100)
        self.addPermanentWidget(self.edit, 100)
        self.addPermanentWidget(self.detail)
        self.addPermanentWidget(self.model)
        self.addPermanentWidget(self.page, 0)

        self.info.hide()
        self.edit.hide()
        self.detail.hide()

        self.setSizeGripEnabled(False)
        self.setStyleSheet(self.style_sheet)

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        self.info.installEventFilter(listener)
        self.detail.installEventFilter(listener)
        self.model.installEventFilter(listener)

    def removeEventFilter(self, listener):

        super().removeEventFilter(listener)
        self.info.removeEventFilter(listener)
        self.edit.removeEventFilter(listener)
        self.detail.removeEventFilter(listener)
        self.model.removeEventFilter(listener)

    def on_hashChanged(self, document): 

        if document.hash(): 
            self.model.setText(str(document.hash()))

    def on_viewChanged(self, view): 

        if view.name(): self.model.setText(str(view.name()))

    def on_itemChanged(self, view, item=None): 

        cpage=view.currentPage()
        pages=view.totalPages()
        self.page.setText(f'[{cpage}/{pages}]')

    @register('i', modes=['normal', 'command'])
    def toggle(self):

        if self.isVisible():
            self.hide()
        else:
            self.show()

        self.toggled.emit(self.isVisible())

    def clear(self, fields=['info', 'edit', 'detail']):

        for f in fields:
            field=getattr(self, f)
            field.setText('')
            field.hide()

    def setData(self, data={}):

        self.clear()

        for f, v in data.items():

            if f=='mode': v=f"[{v}]"
            field=getattr(self, f, None)
            if field:
                field.setText(v)
                field.show()

    def keyPressEvent(self, event):

        self.keyPressed.emit(event) 
        if event.key()==QtCore.Qt.Key_Escape: 
            self.hideWanted.emit() 
