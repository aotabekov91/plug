import sys
from PyQt5 import QtCore
from gizmo.ui import Display
from gizmo.ui import Application
from gizmo.widget import CommandStack 
from plug.utils import setKeys
from plug.qt.utils.buffer import Buffer

from .stack_window import StackWindow

class UIMan(QtCore.QObject):

    def __init__(
            self, obj=None, **kwargs):

        self.obj=obj
        self.qapp=None
        self.window=None
        self.current=None
        self.kwargs=kwargs
        self.command_activated=False
        super().__init__(obj)

    def setApp(self):

        self.qapp=Application([])
        self.qapp.setApplicationName(
                self.obj.name)
        self.obj.setParent(self.qapp)

    def setAppUI(
            self, 
            buffer_class=Buffer,
            display_class=Display,
            ):

        self.window=StackWindow(
                objectName='MainWindow')
        self.buffer=buffer_class()
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

    def setUI(self, ui=CommandStack(), obj=None): 

        obj=obj or self.obj
        ui.hide()
        obj.ui=ui
        ui.mode=obj
        ui.setObjectName(obj.name.title())
        if hasattr(ui, 'hideWanted'):
            ui.hideWanted.connect(obj.deactivate)
        if hasattr(ui, 'keysChanged'):
            ui.keysChanged.connect(obj.keysChanged)
        if hasattr(ui, 'modeWanted'):
            ui.modeWanted.connect(obj.modeWanted)
        if hasattr(ui, 'delistenWanted'):
            ui.delistenWanted.connect(obj.delistenWanted)
        if hasattr(ui, 'focusGained'):
            f=lambda **kwargs: obj.focusGained.emit(obj) 
            ui.focusGained.connect(f)
        if hasattr(ui, 'focusLost'):
            f=lambda **kwargs: obj.focusLost.emit(obj) 
            ui.focusLost.connect(f)
        self.locate(obj)

    def setUIKeys(self, ui=None, obj=None):

        def cleanupPrev(widget, name):

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
                cleanupPrev(widget, k)
            setKeys(widget, keys)
            ear=getattr(widget, 'ear', None)
            if ear: ear.saveOwnKeys()

        obj=obj or self.obj
        ui=getattr(obj, 'ui', None)
        keys=obj.config.get('Keys', {})
        ui_keys=keys.get('UI', {})
        if ui and ui_keys:
            setWidgetKeys(ui_keys, ui)

    def locate(self, obj=None):

        obj=obj or self.obj
        ui=getattr(obj, 'ui', None)
        pos=getattr(obj, 'position', None)
        if ui and pos:
            w=self.window
            pos=pos.split('_')
            if len(pos)==1:
                if pos[0]=='window':
                    w.stack.addWidget(ui, obj.name) 
                elif pos[0]=='overlay':
                    ui.setParent(w.overlay)
            else:
                if pos[0]=='dock':
                    ds=['up', 'down', 'left', 'right']
                    if pos[1] in ds:
                        w.docks.setTab(ui, pos[1])

    def delocate(self, obj=None):

        obj = obj or self.obj
        ui=getattr(obj, 'ui', None)
        if obj.position=='window':
            self.window.remove(ui)
        if obj.position=='dock':
            self.window.docks.delTab(ui)

    def relocate(self, position, obj=None):

        obj=obj or self.obj
        ob.position=position
        self.delocateUI()
        self.locate()

    def activate(self, obj=None):

        obj=obj or self.obj
        ui=getattr(obj, 'ui', None)
        window=getattr(obj, 'window', None)
        if window:
            window.show()
            sys.exit(self.qapp.exec_())
        elif ui:
            if hasattr(ui, 'dock'):
                ui.dock.activate(ui)
            elif obj.position=='overlay':
                ui.show()
            elif obj.position=='window':
                self.window.show(ui)

    def deactivate(self, obj=None):

        obj=obj or self.obj
        ui=getattr(obj, 'ui', None)
        window=getattr(obj, 'window', None)
        if window: 
            sys.exit()
        elif ui:
            if hasattr(ui, 'dock'):
                ui.dock.deactivate(ui)
            elif obj.position=='overlay':
                ui.hide()
            elif obj.position=='window':
                self.window.show()

    def listen(self, obj=None):

        obj = obj or self.obj
        ui=getattr(obj, 'ui', None)
        if ui: ui.setFocus()

    def delisten(self, obj=None):

        if self.obj: 
            self.window.setFocus()
