from ..base import Mode

class Input(Mode):

    def __init__(self, app):

        super().__init__(app=app, 
                         listen_leader='i', 
                         show_statusbar=True,
                         delisten_on_exec=False,
                         )

    def activateCheck(self, event):

        leaderPressed=super().activateCheck(event)
        if leaderPressed: 
            if self.app.modes.normal.listening:
                return len(self.app.modes.normal.keys_pressed)==0
