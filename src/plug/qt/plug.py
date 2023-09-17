from PyQt5 import QtCore, QtWidgets

from plug import Plug as BasePlug
from gizmo.widget import CommandStack 
from plug.qt.utils import EventListener

class Plug(BasePlug, QtCore.QObject):

    endedListening=QtCore.pyqtSignal(object)
    startedListening=QtCore.pyqtSignal(object)

    forceDelisten=QtCore.pyqtSignal()
    delistenWanted=QtCore.pyqtSignal()
    modeWanted=QtCore.pyqtSignal(object)
    listenWanted=QtCore.pyqtSignal(object)
    escapePressed=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    keysChanged=QtCore.pyqtSignal(str)
    keyPressed=QtCore.pyqtSignal(object, object)

    def __init__(self, *args, **kwargs):

        self.listening=False
        self.command_activated=False

        self.app=kwargs.get('app', None)
        self.position=kwargs.get('position', None)
        self.follow_mouse=kwargs.get('follow_mouse', False)

        argv=kwargs.get('argv', None)
        if argv:
            super(QtWidgets.QApplication, self).__init__(
                    argv)
        else:
            super(QtCore.QObject, self).__init__()

        super(BasePlug, self).__init__(*args, **kwargs)

    def setup(self):

        super().setup()
        self.setActions()
        if self.app: 
            self.app.plugman.add(self)
            self.setEventListener(**self.kwargs)

    def setEventListener(self, **kwargs):

        self.event_listener=EventListener(
                obj=self, app=self.app, **kwargs)

    def toggleCommandMode(self):

        if self.command_activated:
            self.deactivateCommandMode()
        else:
            self.activateCommandMode()

    def deactivateCommandMode(self):

        if hasattr(self, 'ui'):
            self.command_activated=False
            if self.ui.current==self.ui.commands: 
                self.ui.show(self.ui.previous)

    def activateCommandMode(self):

        if hasattr(self, 'ui'):
            self.command_activated=True
            self.ui.show(self.ui.commands)

    def listen(self): 

        self.listening=True
        self.event_listener.listen()
        if hasattr(self, 'ui') and self.activated: 
            self.ui.setFocus()
        self.startedListening.emit(self)

    def delisten(self): 

        self.listening=False
        self.event_listener.delisten()
        self.endedListening.emit(self)

    def checkLeader(self, event, pressed=None): 

        l=self.event_listener.listen_leader
        return pressed in l

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
