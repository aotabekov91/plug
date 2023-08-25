from PyQt5 import QtWidgets, QtCore

from gizmo.widget import CommandStack 

from .base import Plug

class PlugObj(Plug, QtCore.QObject):

    forceDelisten=QtCore.pyqtSignal()
    delistenWanted=QtCore.pyqtSignal()
    modeWanted=QtCore.pyqtSignal(object)
    listenWanted=QtCore.pyqtSignal(object)
    returnPressed=QtCore.pyqtSignal()
    keyPressed=QtCore.pyqtSignal(object, object)

    def __init__(self,
                 position=None,
                 listen_port=False, 
                 follow_mouse=True,
                 **kwargs):

        self.bar_data={}
        self.listening=False
        self.position=position
        self.follow_mouse=follow_mouse

        super(PlugObj, self).__init__(
                listen_port=listen_port,
                **kwargs)

        self.register()

    def setup(self):

        super().setup()
        if self.app: 
            self.app.plugman.add(self, 'plug')
            self.setFilter()

    def setFilter(self):

        self.app.installEventFilter(self)

    def setUI(self): 

        self.ui=CommandStack()
        self.ui.hideWanted.connect(self.on_uiHideWanted)
        self.ui.focusGained.connect(self.on_uiFocusGained)
        self.locateUI()

    def locateUI(self):

        if hasattr(self, 'ui'):
            dock=['left', 'right', 'top', 'bottom']
            if self.position=='window':
                self.app.window.add(self.ui, self.name) 
            elif self.position=='overlay':
                pass
            elif self.position in dock:
                self.app.window.docks.setTab(
                        self.ui, self.position)

    def delocateUI(self):

        if self.position=='window':
            self.app.window.remove(self.ui)
        if self.position=='dock':
            self.app.window.docks.delTab(self.ui)

    def relocateUI(self, position):

        self.position=position
        self.delocateUI()
        self.locateUI()

    def checkListen(self, event):

        modes=self.app.plugman.getModes().items()
        for name, mode in modes:
            if mode.checkKey(event): return mode

    def checkMode(self, widget, event):

        mode=self.checkListen(event)
        if mode:
            if mode==self:
                self.delistenWanted.emit()
            else:
                self.modeWanted.emit(mode)
            return True
        return False

    def eventFilter(self, widget, event):

        c1=event.type()==QtCore.QEvent.KeyPress
        if self.listening and c1: 
            if self.checkMode(widget, event):
                event.accept()
                return True
            return super().eventFilter(widget, event)
        return False

    def on_uiFocusGained(self):

        if self.follow_mouse: self.modeWanted.emit(self)

    def on_uiHideWanted(self):

        self.delistenWanted.emit()
        self.deactivate()

    def listen(self): 

        self.listening=True
        if hasattr(self, 'ui') and self.activated: 
            self.ui.setFocus()

    def delisten(self): 

        self.listening=False

    def activate(self):

        self.activated=True
        self.listenWanted.emit(self)

        if hasattr(self, 'ui'): 
            if hasattr(self.ui, 'dock'):
                self.ui.dock.activate(self.ui)
            elif self.position=='window':
                self.app.window.show(self.ui)
            elif self.position=='overlay':
                self.ui.show()

    def deactivate(self):

        self.activated=False
        if hasattr(self, 'ui'): 
            if hasattr(self.ui, 'dock'):
                self.ui.dock.deactivate(self.ui)
            elif self.position=='window':
                self.app.window.show(self.app.window.main)
            elif self.position=='overlay':
                self.ui.hide()

    def register(self):

        if self.app: 
            self.app.plugman.register(self, self.actions)
