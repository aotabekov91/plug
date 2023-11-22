import sys
from gizmo.ui import Display
from plug.utils import setKeys
from PyQt5 import QtCore, QtWidgets
from gizmo.widget import StackedWidget
from plug.qt.utils.buffer import Buffer

from .stack_window import StackWindow

class UIMan(QtCore.QObject):
    
    appLaunched=QtCore.pyqtSignal()
    appSoonQuits=QtCore.pyqtSignal()
    viewOctivated=QtCore.pyqtSignal()
    viewActivated=QtCore.pyqtSignal(object)

    def __init__(self):

        self.app=None
        self.m_widgets=[]
        self.launch_wait=10
        super().__init__()
        self.setTimer()

    def setTimer(self):

        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(
                self.appLaunched.emit)
        self.timer.setSingleShot(True)

    def setupUIKeys(self, obj, ui=None):

        name='ui'
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

        ui=getattr(obj, name, None)
        keys=obj.config.get('Keys', {})
        ui_keys=keys.get('UI', {})
        if ui and ui_keys:
            setWidgetKeys(ui_keys, ui)

    def setApp(self, obj):

        self.app=obj
        self.setParent(obj)
        obj.qapp=QtWidgets.QApplication([])
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
        obj.buffer, obj.ui, obj.display=b, w, d
        self.m_widgets+=[obj.ui, obj.display]

    def setupUI(self, obj, ui, name='ui', **kwargs): 

        ui.hide()
        self.m_widgets+=[ui]
        self.locate(obj, ui, name)
        ui.setObjectName(obj.name.title())
        if hasattr(ui, 'focusGained'):
            f=lambda **kwargs: obj.focusGained.emit(obj) 
            ui.focusGained.connect(f)
        if hasattr(ui, 'focusLost'):
            f=lambda **kwargs: obj.focusLost.emit(obj) 
            ui.focusLost.connect(f)

    def locate(self, obj, ui, name):

        pos=getattr(obj, 'position', {})
        loc=pos.get(name, None)
        if not loc: return
        ui.pos=loc
        loc=loc.split('_')
        w=self.app.ui
        if len(loc)==1:
            if loc[0]=='window':
                w.stack.addWidget(
                        ui, obj.name) 
            elif loc[0]=='overlay':
                ui.setParent(
                        w.overlay)
        else:
            if loc[0]=='dock':
                ds=['up', 'down', 'left', 'right']
                if loc[1] in ds: 
                    w.docks.setTab(ui, loc[1])

    def delocate(self, obj, name='ui'):

        p=obj.position
        ui=getattr(obj, name, None)
        if p=='window':
            self.app.ui.remove(ui)
        elif p=='dock':
            self.app.ui.docks.delTab(ui)

    def relocate(self, obj, position):

        obj.position=position
        self.delocateUI()
        self.locate(obj)

    def activate(self, obj, ui=None, **kwargs):

        ui = ui or getattr(obj, 'ui', None)
        if obj.main_app:
            ui.show()
            self.timer.start(self.launch_wait)
            sys.exit(obj.qapp.exec_())
        elif ui:
            p=getattr(ui, 'pos', None)
            if p=='overlay':
                ui.show(**kwargs)
            elif p=='window':
                self.app.ui.show(
                        ui, **kwargs)
            elif p=='display':
                self.app.display.setupView(
                        ui, **kwargs)
            elif hasattr(ui, 'dock'):
                ui.dock.activate(
                        ui, **kwargs)
            self.viewActivated.emit(ui)

    def deactivate(self, obj, ui=None):

        ui = ui or getattr(obj, 'ui', None)
        if obj.main_app: 
            self.appSoonQuits.emit()
            sys.exit()
        elif ui:
            pos=getattr(ui, 'pos', None)
            if hasattr(ui, 'dock'):
                ui.dock.deactivate(ui)
            elif pos=='overlay':
                ui.hide()
            elif pos=='window':
                self.app.ui.show()
            self.viewOctivated.emit()

    def focus(self, obj):

        name='ui'
        ui=getattr(obj, name, None)
        if ui: ui.setFocus()

    def defocus(self, obj):
        self.app.ui.setFocus()
