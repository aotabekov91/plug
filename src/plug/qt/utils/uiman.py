import sys
from functools import partial
from plug.utils import setKeys
from PyQt5 import QtCore, QtWidgets
from gizmo.ui import TabbedTileDisplay
from plug.qt.utils.buffer import Buffer

from .stack_window import StackWindow

class UIMan(QtCore.QObject):
    
    appLaunched=QtCore.pyqtSignal()
    appSoonQuits=QtCore.pyqtSignal()
    viewOctivated=QtCore.pyqtSignal()
    viewActivated=QtCore.pyqtSignal(object)

    def __init__(self):

        self.app=None
        self.m_wait=10
        self.m_active={}
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

    def active(self):
        return self.m_active

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
            window_class=StackWindow,
            display_class=TabbedTileDisplay,
            ):

        b=buffer_class()
        w=window_class(objectName='MainWindow')
        d=display_class(app=obj, window=w)
        w.main.m_layout.addWidget(d)
        obj.buffer, obj.ui, obj.display=b, w, d

    def setupUI(
            self, 
            obj=None, 
            ui=None, 
            name='ui', 
            **kwargs): 

        ui.hide()
        ui = ui or getattr(obj, name, None)
        self.locate(obj, ui, name)
        if obj:
            ui.setObjectName(obj.name.title())
        if hasattr(ui, 'focusGained'):
            if obj:
                f=lambda **kwargs: obj.focusGained.emit(obj) 
                ui.focusGained.connect(f)
            ui.focusGained.connect(
                    partial(self.saveActiveView, view=ui))
        if hasattr(ui, 'focusLost'):
            if obj:
                f=lambda **kwargs: obj.focusLost.emit(obj) 
                ui.focusLost.connect(f)

    def locate(self, obj, ui, name):

        pos={}
        if ui:
            p=getattr(ui, 'position', {})
            pos.update(p)
        if obj:
            p=getattr(obj, 'position', {})
            pos.update(p)
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
                ui.setParent(w.overlay)
        else:
            if loc[0]=='dock':
                ds=['up', 'down', 'left', 'right']
                if loc[1] in ds: 
                    ui.isDockView=True
                    w.docks.setTab(ui, loc[1])

    def delocate(self, ui=None):

        if ui and ui.position=='window':
            self.app.ui.remove(ui)
        elif ui and ui.position=='dock':
            self.app.ui.docks.delTab(ui)

    def relocate(self, ui, position):

        self.delocate(ui=ui)
        ui.position=position
        self.locate(ui=ui)

    def activate(
            self, 
            obj=None, 
            ui=None, 
            **kwargs):

        ui = ui or getattr(obj, 'ui', None)
        if obj and obj.isMainApp:
            ui.show()
            self.timer.start(self.m_wait)
            sys.exit(obj.qapp.exec_())
        elif not ui is None:
            p=getattr(ui, 'pos', None)
            if p=='overlay':
                ui.show(**kwargs)
                up=getattr(ui, 'updatePosition', None)
                if up: up()
            elif p=='window':
                self.app.ui.show(
                        ui, **kwargs)
            elif p=='display':
                self.app.display.setupView(
                        ui, **kwargs)
            elif hasattr(ui, 'dock'):
                ui.dock.activate(ui)
            ui.setFocus()
            # self.m_active[id(ui)]=ui
            # self.viewActivated.emit(ui)

    def saveActiveView(self, view):

        self.m_active[id(view)]=view
        self.viewActivated.emit(view)

    # def waveActiveView(self, ui):
    #     self.m_active[id(ui)]=ui
    #     self.viewActivated.emit(ui)

    def octivate(
            self, 
            obj=None, 
            ui=None,
            **kwargs):

        ui = ui or getattr(obj, 'ui', None)
        if obj and obj.isMainApp: 
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
            self.m_active.pop(id(ui), None)

    def focus(self, obj):

        name='ui'
        ui=getattr(obj, name, None)
        if ui: ui.setFocus()

    def defocus(self, obj):
        self.app.ui.setFocus()

    def split(self, view=None, **kwargs):

        v, p = self.getParent(view)
        if p and hasattr(p, 'canSplit'): 
            p.split(view=v, **kwargs)

    def move(
            self, 
            view=None, 
            vkind='view', 
            **kwargs
            ):

        if vkind=='view':
            v, p = self.getParent(view)
            if p and hasattr(p, 'canMove'): 
                p.move(view=v, **kwargs)
        elif vkind=='tab':
            t=self.getTabber()
            if t: t.tabMove(**kwargs)

    def goTo(
            self, 
            view=None, 
            vkind='view', 
            **kwargs
            ):
        
        if vkind=='view':
            v, p = self.getParent(view)
            if p and hasattr(p, 'canGo'): 
                p.goTo(view=v, **kwargs)
        elif vkind=='tab':
            t=self.getTabber()
            if t: t.tabGoTo(**kwargs)

    def add(
            self, 
            view=None, 
            vkind='view', 
            **kwargs):

        if vkind=='tab':
            t=self.getTabber()
            if t: t.tabAddNew(**kwargs)
            
    def close(
            self, 
            view=None, 
            vkind='view', 
            **kwargs):

        if vkind=='view':
            v, p = self.getParent(view)
            if p and hasattr(p, 'canCloseView'): 
                p.closeView(view=v, **kwargs)
        elif vkind=='tab':
            t=self.getTabber()
            if t: t.tabClose(**kwargs)

    def scale(self, view=None, **kwargs):

        v, p = self.getParent(view)
        if p and hasattr(p, 'canScale'): 
            p.scale(view=v, **kwargs)

    def toggleFullscreen(
            self,
            view=None,
            vkind=None,
            **kwargs,
            ):

        if vkind=='app':
            self.toggleAppFullscreen()
        else:
            v, p = self.getParent(view)
            if v.check('canFullscreen'):
                v.toggleFullscreen()

            # if p and not hasattr(p, 'canFullscreen'): 
            #     p=self.getTabber(v)
            # if p and hasattr(p, 'canFullscreen'): 
            #     p.toggleFullscreen(view=v, **kwargs)

    def toggleAppFullscreen(self): 

        s=self.app.ui.windowState()
        if (s & QtCore.Qt.WindowFullScreen):
            s=QtCore.Qt.WindowNoState
        else:
            s=QtCore.Qt.WindowFullScreen
        self.app.ui.setWindowState(s)

    def getParent(self, view=None):

        v = view or self.app.handler.view()
        p = v.parent()
        if v and hasattr(v, 'isDockView'):
            return v, self.app.ui.docks
        elif v and hasattr(p, 'isDockView'):
            return v, self.app.ui.docks
        elif v and hasattr(v, 'isDisplayView'):
            return v, v.parent() 
        return v, self.getTabber(view)

    def getTabber(self, view=None):

        v= view or self.app.handler.view()
        if v and v.check('hasTabs'):
            return v
        if v and v.check('hasTabber'):
            return v.m_tabber
