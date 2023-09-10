from gizmo.utils import EventListener as Base

class EventListener(Base):

    def __init__(
            self, 
            leader='.',
            listening=False,
            **kwargs,
            ):

        super().__init__(
                leader=leader,
                listening=listening,
                **kwargs)

    def checkLeader(self, event):

        if self.app:
            ms=self.app.plugman.plugs.items()
            for _, m in ms:
                f=getattr(m, 'checkLeader', None)
                if not f: continue 
                if m.checkLeader(event, (self.pressed,)):
                    if m==self.obj:
                        self.delistenWanted.emit()
                    else:
                        self.modeWanted.emit(m)
                    return True
        return super().checkLeader(event)
