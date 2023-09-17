from gizmo.utils import EventListener as Base

class EventListener(Base): pass

    # def toggleMode(self, mode):

    #     if mode==self.obj:
    #         self.delistenWanted.emit()
    #     else:
    #         self.modeWanted.emit(mode)

    # def checkLeader(self, event):

    #     if self.app:
    #         ms=self.app.plugman.plugs.items()
    #         for _, m in ms:
    #             f=getattr(m, 'checkLeader', None)
    #             if not f: continue 
    #             if m.checkLeader(event, (self.pressed,)):
    #                 self.timer.stop()
    #                 self.timer.timeout.disconnect()
    #                 func=lambda: self.toggleMode(m)
    #                 self.timer.timeout.connect(func)
    #                 self.timer.start(self.wait_run)
    #                 return True
    #     return super().checkLeader(event)


