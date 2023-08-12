from PyQt5 import QtWidgets, QtCore

from .base import Plug
from ..widget import CommandStack 

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
                 listen_leader=None,
                 follow_mouse=True,
                 **kwargs):

        self.listening=False
        self.position=position
        self.follow_mouse=follow_mouse
        self.listen_leader=self.setKey(listen_leader)

        super(PlugObj, self).__init__(
                listen_port=listen_port,
                **kwargs)

        self.register()

    def setup(self):

        super().setup()
        if self.app: 
            self.app.modes.addMode(self)
            self.app.installEventFilter(self)

    def setUI(self): 

        self.ui=CommandStack()
        self.ui.hideWanted.connect(self.on_uiHideWanted)
        self.ui.focusGained.connect(self.on_uiFocusGained)

        self.ui.keyPressed
        self.locateUI()

    def locateUI(self):

        if hasattr(self, 'ui'):

            dock=['left', 'right', 'top', 'bottom']
            if self.position=='window':
                self.app.stack.add(self.ui, self.name) 
            elif self.position=='overlay':
                pass
            elif self.position in dock:
                self.app.main.docks.setTab(
                        self.ui, self.position)

    def delocateUI(self):

        if self.position=='window':
            self.app.stack.remove(self.ui)
        if self.position=='dock':
            self.app.main.docks.delTab(self.ui)

    def relocateUI(self, position):

        self.position=position
        self.delocateUI()
        self.locateUI()

    def eventFilter(self, widget, event):

        c1=event.type()==QtCore.QEvent.KeyPress
        if self.listening and c1: 

            mode=self.checkListen(event)
            if mode:
                if mode==self:
                    self.delistenWanted.emit()
                else:
                    self.modeWanted.emit(mode)
                event.accept()
                return True
            return super().eventFilter(widget, event)
        return False

    def checkListen(self, event):

        for mode in self.app.modes.getModes():
            if mode.checkKey(event, mode.listen_leader): 
                return mode

    def on_uiFocusGained(self):

        if self.follow_mouse: self.modeWanted.emit(self)

    def on_uiHideWanted(self):

        self.delistenWanted.emit()
        self.deactivate()

    def listen(self): 

        self.listening=True
        if hasattr(self, 'ui') and self.activated: 
            self.ui.setFocus()

    def delisten(self): self.listening=False

    def activate(self):

        self.activated=True
        self.listenWanted.emit(self)
        if hasattr(self, 'ui'): 
            if hasattr(self.ui, 'dock'):
                self.ui.dock.activate(self.ui)
            elif self.position=='window':
                pass
            elif self.position=='overlay':
                self.ui.show()

    def deactivate(self):

        self.activated=False
        if hasattr(self, 'ui'): 
            if hasattr(self.ui, 'dock'):
                self.ui.dock.deactivate(self.ui)
            elif self.position=='window':
                pass
            elif self.position=='overlay':
                self.ui.hide()

    def setShortcuts(self):

        if self.config.has_section('Shortcuts'):
            shortcuts=dict(self.config['Shortcuts'])
            for func_name, key in shortcuts.items():
                func=getattr(self, func_name, None)
                if func and hasattr(func, 'widget'): 
                    if func.widget=='window':
                        widget=self.app.main
                    elif func.widget=='display':
                        widget=self.app.main.display
                    else:
                        setattr(func, 'key', key)
                        continue
                    context=getattr(
                            func, 
                            'context', 
                            QtCore.Qt.WidgetWithChildrenShortcut)
                    shortcut=QtWidgets.QShortcut(widget)
                    shortcut.setKey(key)
                    shortcut.setContext(context)
                    shortcut.activated.connect(func)

    def register(self):

        if self.app: 
            self.app.manager.register(self, self.actions)
