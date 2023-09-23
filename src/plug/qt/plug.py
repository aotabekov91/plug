import sys
from PyQt5 import QtCore, QtWidgets

from plug import Plug as Base
from plug.utils import setKeys
from plug.qt.utils import Plugman

from gizmo.ui import StackWindow
from gizmo.utils import EventListener
from gizmo.widget import CommandStack 

class Plug(Base, QtCore.QObject):

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

        self.qapp=None
        self.listening=False
        self.command_activated=False

        self.app=kwargs.get('app', None)
        self.position=kwargs.get('position', None)
        self.follow_mouse=kwargs.get('follow_mouse', False)

        super(Plug, self).__init__(*args, **kwargs)

    def setApp(self):

        self.qapp=QtWidgets.QApplication([])
        self.setParent(self.qapp)

    def setAppUI(self, 
                 display_class=None, 
                 view_class=None):

        self.window=StackWindow(
                self, 
                display_class, 
                view_class)

    def setName(self):

        super().setName()
        if self.qapp:
            self.qapp.setApplicationName(self.name)

    def initialize(self):

        super().initialize()
        self.setUIKeys()
        if self.qapp:
            self.plugman.loadPicks()

    def setup(self):

        super().setup()
        if self.qapp: 
            self.setPlugman(plugman=Plugman)
            self.event_timer=QtCore.QTimer()
        if self.app:
            self.app.plugman.add(self)
            self.setEar()

    def setEar(self):

        kwargs=self.kwargs.copy()
        settings=self.config.get('Settings', {})
        kwargs.update(settings)
        self.ear=EventListener(
                obj=self, listening=False, **kwargs)

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
        self.ear.listen()
        if hasattr(self, 'ui') and self.activated: 
            self.ui.setFocus()
        self.startedListening.emit(self)

    def delisten(self): 

        self.listening=False
        self.ear.delisten()
        self.endedListening.emit(self)

    def checkLeader(self, event, pressed=None): 

        return pressed in self.ear.listen_leader

    def setUI(self, ui=None): 

        if ui is None: 
            ui=CommandStack()

        self.ui=ui
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

    def setUIKeys(self, ui=None):

        def setWidgetKeys(keys, widget):
            print(widget, keys)
            for k, v in keys.items():
                if type(v)==str:
                    setKeys(widget, keys)
                    ear=getattr(widget, 'ear', None)
                    if ear: ear.saveOwnKeys()
                elif type(v)==dict:
                    widget=getattr(widget, k, None)
                    if widget: setKeys(widget, v)
            self.setUIKeys(ui)

        ui=getattr(self, 'ui', None)
        keys=self.config.get('Keys', {})
        ui_keys=keys.get('UI', {})
        print(self.name, ui, ui_keys)
        if ui and ui_keys:
            setWidgetKeys(ui_keys, ui)

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
                self.app.window.add(
                        self.ui, self.name) 
            elif self.position in dock:
                self.app.window.docks.setTab(
                        self.ui, self.position)
            elif self.position=='overlay':
                pass

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
        self.modeWanted.emit(self)
        self.activateUI()

    def deactivate(self):

        self.activated=False
        self.deactivateUI()
        if self.listening:
            self.delistenWanted.emit()

    def run(self):

        super().run()
        if self.qapp:
            if hasattr(self, 'window'): 
                self.window.show()
            sys.exit(self.qapp.exec_())

    def exit(self): 

        super().exit()
        if self.qapp:
            sys.exit()
