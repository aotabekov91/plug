from PyQt6 import QtCore

from gizmo.utils import EventListener as Base

class EventListener(Base):

    def __init__(
            self, 
            leader='.',
            **kwargs,
            ):

        super().__init__(
                leader=leader,
                **kwargs)
        self.listening=False

    def eventFilter(self, widget, event):

        if event.type()!=QtCore.QEvent.KeyPress:
            return False
        elif not self.listening:
            return False
        elif self.checkMode(event):
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

    def listen(self):

        self.listening=True
        self.clearKeys()

    def delisten(self):

        self.listening=False
        self.timer.stop()
        self.clearKeys()
