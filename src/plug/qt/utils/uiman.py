import sys
from PyQt5 import QtCore, QtWidgets

from plug.utils import setKeys
from gizmo.ui import StackWindow
from gizmo.widget import CommandStack 

class UIMan(QtCore.QObject):

    def __init__(self, 
                 obj, 
                 app=None,
                 **kwargs):

        super().__init__(obj)

        self.obj=obj
        self.app=app
        self.ui=None
        self.qapp=None
        self.window=None
        self.kwargs=kwargs
        self.command_activated=False
        self.position=kwargs.get('position', None)

    def setApp(self):

        self.qapp=QtWidgets.QApplication([])
        self.qapp.setApplicationName(
                self.obj.name)
        self.obj.setParent(self.qapp)

    def setAppUI(self, display_class, buffer_class):

        self.window=StackWindow()
        self.buffer=buffer_class(self)
        self.display=display_class(self)
        self.window.main.m_layout.addWidget(
                self.display)
        self.obj.buffer=self.buffer
        self.obj.window=self.window
        self.obj.display=self.display

    def setUI(self, ui=None): 

        if ui is None: 
            ui=CommandStack()

        self.ui=ui
        self.obj.ui=self.ui
        self.ui.setObjectName(self.obj.name)
        if hasattr(self.ui, 'hideWanted'):
            self.ui.hideWanted.connect(
                    self.on_uiHideWanted)
        if hasattr(self.ui, 'focusGained'):
            self.ui.focusGained.connect(
                    self.on_uiFocusGained)
        if hasattr(self.ui, 'keyPressed'):
            self.ui.keyPressed.connect(
                    self.obj.keyPressed)
        if hasattr(self.ui, 'keysChanged'):
            self.ui.keysChanged.connect(
                    self.obj.keysChanged)
        if hasattr(self.ui, 'modeWanted'):
            self.ui.modeWanted.connect(
                    self.obj.modeWanted)
        if hasattr(self.ui, 'delistenWanted'):
            self.ui.delistenWanted.connect(
                    self.obj.delistenWanted)
        if hasattr(self.ui, 'forceDelisten'):
            self.ui.forceDelisten.connect(
                    self.obj.forceDelisten)
        self.locate()

    def setUIKeys(self, ui=None):

        def cleanPrevious(widget, name):

            ear=getattr(widget, 'ear', None)
            if ear:
                m=ear.matches.get(name, None)
                ear.commands.pop(m)

        def setWidgetKeys(keys, widget):

            for k, v in keys.items():
                if type(v)==dict:
                    widget=getattr(widget, k, None)
                    if widget: setWidgetKeys(v, widget)
                    return
                cleanPrevious(widget, k)
            setKeys(widget, keys)
            ear=getattr(widget, 'ear', None)
            if ear: 
                ear.saveOwnKeys()

        ui=getattr(self, 'ui', None)
        keys=self.obj.config.get('Keys', {})
        ui_keys=keys.get('UI', {})
        if ui and ui_keys:
            setWidgetKeys(ui_keys, ui)

    def on_uiFocusGained(self):

        if self.obj.follow_mouse: 
            self.obj.modeWanted.emit(self.obj)

    def on_uiHideWanted(self):

        self.obj.deactivate()
        self.obj.delistenWanted.emit()

    def locate(self):

        if self.ui:
            dock=['left', 'right', 'top', 'bottom']
            if self.position=='window':
                self.app.window.add(
                        self.ui, self.name) 
            elif self.position in dock:
                self.app.window.docks.setTab(
                        self.ui, self.position)
            elif self.position=='overlay':
                pass

    def delocate(self):

        if self.position=='window':
            self.app.window.remove(
                    self.ui)
        if self.position=='dock':
            self.app.window.docks.delTab(
                    self.ui)

    def relocate(self, position):

        self.position=position
        self.delocateUI()
        self.locate()

    def activate(self): 

        if self.window:
            self.window.show()
            sys.exit(self.qapp.exec_())
        elif self.ui:
            if hasattr(self.ui, 'dock'):
                self.ui.dock.activate(self.ui)
            elif self.position=='window':
                self.window.show(self.ui)
            elif self.position=='overlay':
                self.ui.show()

    def deactivate(self):

        if self.window:
            sys.exit()
        elif self.ui:
            if hasattr(self.ui, 'dock'):
                self.ui.dock.deactivate(self.ui)
            elif self.position=='window':
                self.window.show(self.window.main)
            elif self.position=='overlay':
                self.ui.hide()

    def listen(self):

        if self.ui: 
            self.ui.setFocus()

    def delisten(self):

        if self.app:
            self.app.window.setFocus()