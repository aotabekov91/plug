from PyQt5 import QtCore

from gizmo.utils import EventListener as Base

class EventListener(Base):

    def __init__(
            self, 
            leader='.',
            special=[],
            **kwargs,
            ):

        super().__init__(
                leader=leader,
                **kwargs)
        self.listening=False
        self.special=special

    def eventFilter(self, widget, event):

        if event.type()!=QtCore.QEvent.KeyPress:
            return False
        elif not self.listening:
            return False
        elif self.checkMode(event):
            event.accept()
            return True
        elif self.checkSpecialCharacters(event):
            event.accept()
            return True
        return super().eventFilter(widget, event)

    def checkMode(self, event):

        if self.app:
            ms=self.app.plugman.plugs.items()
            for _, m in ms:
                if m.checkLeader(event):
                    if m==self.obj:
                        self.delistenWanted.emit()
                    else:
                        self.modeWanted.emit(m)
                    return True
        return False

    def checkSpecialCharacters(self, event):

        special=None
        enter=[QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]
        if event.key() in enter: 
            self.returnPressed.emit()
            special='return'
        elif event.key()==QtCore.Qt.Key_Backspace:
            self.backspacePressed.emit()
            special='backspace'
        elif event.key()==QtCore.Qt.Key_Escape:
            self.escapePressed.emit()
            special='escape'
        elif event.key()==QtCore.Qt.Key_Tab:
            self.tabPressed.emit()
            special='tab'
        elif event.modifiers()==QtCore.Qt.ControlModifier:
            if event.key()==QtCore.Qt.Key_BracketLeft:
                self.escapePressed.emit()
                special='escape_bracket'
            elif event.key()==QtCore.Qt.Key_M:
                self.carriageReturnPressed.emit()
                special='carriage'
        if special in self.special:
            return True
        else:
            return False

    def listen(self):

        self.listening=True
        self.clearKeys()

    def delisten(self):

        self.listening=False
        self.timer.stop()
        self.clearKeys()
