from PyQt5 import QtCore

from gizmo.widget import CommandStack 

from .base import Plug

class PlugObj(Plug, QtCore.QObject):

    def __init__(self,
                 *args,
                 position=None,
                 follow_mouse=True,
                 **kwargs):

        self.position=position
        self.follow_mouse=follow_mouse

        super(Plug, self).__init__(*args, **kwargs)

    def setup(self):

        super().setup()
        if self.app: 
            self.app.plugman.add(self)

    def setUI(self): 

        self.ui=CommandStack()
        self.ui.setObjectName(self.name)
        if hasattr(self.ui, 'hideWanted'):
            self.ui.hideWanted.connect(
                    self.on_uiHideWanted)
        if hasattr(self.ui, 'focusGained'):
            self.ui.focusGained.connect(
                    self.on_uiFocusGained)
        if hasattr(self.ui, 'keyPressed'):
            self.ui.keyPressed.connect(
                    self.keyPressed)
        if hasattr(self.ui, 'keysChanged'):
            self.ui.keysChanged.connect(
                    self.keysChanged)
        if hasattr(self.ui, 'modeWanted'):
            self.ui.modeWanted.connect(
                    self.modeWanted)
        if hasattr(self.ui, 'delistenWanted'):
            self.ui.delistenWanted.connect(
                    self.delistenWanted)
        if hasattr(self.ui, 'forceDelisten'):
            self.ui.forceDelisten.connect(
                    self.forceDelisten)
        self.locateUI()

    def on_uiFocusGained(self):

        if self.follow_mouse: 
            self.modeWanted.emit(self)

    def on_uiHideWanted(self):

        self.delistenWanted.emit()
        self.deactivate()

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

    def activateUI(self): 

        if hasattr(self, 'ui'): 
            if hasattr(self.ui, 'dock'):
                self.ui.dock.activate(self.ui)
            elif self.position=='window':
                self.app.window.show(self.ui)
            elif self.position=='overlay':
                self.ui.show()

    def deactivateUI(self):

        if hasattr(self, 'ui'): 
            if hasattr(self.ui, 'dock'):
                self.ui.dock.deactivate(self.ui)
            elif self.position=='window':
                self.app.window.show(self.app.window.main)
            elif self.position=='overlay':
                self.ui.hide()

    def activate(self):

        self.activated=True
        self.listenWanted.emit(self)
        self.activateUI()

    def deactivate(self):

        self.activated=False
        self.deactivateUI()
