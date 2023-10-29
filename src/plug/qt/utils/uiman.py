import sys
from PyQt5 import QtCore

from gizmo.ui import Display
from plug.utils import setKeys
from gizmo.widget import CommandStack 
from plug.qt.utils.buffer import Buffer
from gizmo.ui import StackWindow, Application

class UIMan(QtCore.QObject):

    def __init__(
            self, 
            obj, 
            app=None,
            **kwargs
            ):

        self.obj=obj
        self.app=app
        self.ui=None
        self.ears=[]
        self.qapp=None
        self.window=None
        self.current=None
        self.kwargs=kwargs
        self.command_activated=False
        self.position=kwargs.get(
                'position', None)
        super().__init__(obj)

    def setApp(self):

        self.qapp=Application([])
        self.qapp.setApplicationName(
                self.obj.name)
        self.obj.setParent(self.qapp)
        self.qapp.earSet.connect(
                self.on_earSet)
        self.qapp.earGained.connect(
                self.on_earGained)

    def setAppUI(
            self, 
            buffer_class=Buffer,
            display_class=Display,
            ):

        self.window=StackWindow(
                objectName='MainWindow')
        self.buffer=buffer_class(self.obj)
        self.display=display_class(
                app=self.obj,
                window=self.window,
                )
        self.window.main.m_layout.addWidget(
                self.display)
        self.obj.open=self.open
        self.obj.buffer=self.buffer
        self.obj.window=self.window
        self.obj.display=self.display

    def setUI(self, ui=None): 

        if ui is None: 
            ui=CommandStack()
        ui.hide()
        self.ui=ui
        self.obj.ui=self.ui
        self.ui.mode=self.obj
        oname=self.obj.name.title()
        self.ui.setObjectName(oname)
        if hasattr(self.ui, 'hideWanted'):
            self.ui.hideWanted.connect(
                    self.obj.deactivate)
        if hasattr(self.ui, 'focusGained'):
            self.ui.focusGained.connect(
                    self.on_focusGained)
        if hasattr(self.ui, 'focusLost'):
            self.ui.focusLost.connect(
                    self.on_focusLost)
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
                ear.commands.pop(m, None)

        def setWidgetKeys(keys, widget):

            for k, v in keys.items():
                if type(v)==dict:
                    widget=getattr(widget, k, None)
                    if widget: 
                        setWidgetKeys(v, widget)
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

    def locate(self):

        if self.ui and self.position:
            w=self.app.window
            pos=self.position.split('_')
            if len(pos)==1:
                if pos[0]=='window':
                    w.stack.addWidget(
                            self.ui, self.name) 
                elif pos[0]=='overlay':
                    self.ui.setParent(w.overlay)
            else:
                if pos[0]=='dock':
                    ds=['up', 'down', 'left', 'right']
                    if pos[1] in ds:
                        w.docks.setTab(
                                self.ui, pos[1])

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

    def on_earSet(self, ear):
        self.ears+=[ear]

    def on_earGained(self, ear):
        self.current=ear

    def on_focusGained(self, widget=None):
        self.obj.focusGained.emit(self.obj)

    def on_focusLost(self, widget=None):
        self.obj.focusLost.emit(self.obj)

    def open(self, source=None, **kwargs):

        for r in self.obj.renders:
            if r.isCompatible(source):
                r.open(source, **kwargs)
                return
