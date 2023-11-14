import sys
from PyQt5 import QtCore
from gizmo.ui import Display
from plug.utils import setKeys
from gizmo.ui import Application
from gizmo.widget import CommandStack 
from plug.qt.utils.buffer import Buffer

from .stack_window import StackWindow

class UIMan(QtCore.QObject):

    def __init__(self):

        self.app=None
        super().__init__()

    def setApp(self, obj):

        self.app=obj
        self.setParent(obj)
        obj.qapp=Application([])
        obj.qapp.setApplicationName(obj.name)
        obj.setParent(obj.qapp)

    def setAppUI(
            self, 
            obj,
            buffer_class=Buffer,
            display_class=Display,
            window_class=StackWindow,
            ):

        b=buffer_class()
        w=window_class(objectName='MainWindow')
        d=display_class(app=obj, window=w)
        w.main.m_layout.addWidget(d)
        obj.buffer, obj.window, obj.display=b, w, d

    def setUI(self, obj, ui=None): 

        ui = ui or CommandStack()
        ui.hide()
        obj.ui, ui.mode=ui, obj
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

    def setUIKeys(self, obj, ui=None):

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

        ui=getattr(obj, 'ui', None)
        keys=obj.config.get('Keys', {})
        ui_keys=keys.get('UI', {})
        if ui and ui_keys:
            setWidgetKeys(ui_keys, ui)

    def locate(self, obj):

        ui=getattr(obj, 'ui', None)
        pos=getattr(obj, 'position', None)
        if ui and pos:
            w=self.app.window
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

    def delocate(self, obj):

        pos=obj.position
        ui=getattr(obj, 'ui', None)
        if pos=='window':
            self.app.window.remove(ui)
        elif pos=='dock':
            self.app.window.docks.delTab(ui)

    def relocate(self, obj, position):

        ob.position=position
        self.delocateUI()
        self.locate()

    def activate(self, obj):

        ui=getattr(obj, 'ui', None)
        window=getattr(obj, 'window', None)
        if window:
            window.show()
            sys.exit(obj.qapp.exec_())
        elif ui:
            if hasattr(ui, 'dock'):
                ui.dock.activate(ui)
            elif obj.position=='overlay':
                ui.show()
            elif obj.position=='window':
                self.app.window.show(ui)

    def deactivate(self, obj):

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
                self.app.window.show()

    def listen(self, obj):

        ui=getattr(obj, 'ui', None)
        if ui: ui.setFocus()

    def delisten(self, obj):

        w=getattr(obj, 'window', None)
        if w: w.setFocus()
