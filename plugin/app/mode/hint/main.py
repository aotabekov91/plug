from ..base import Mode 

class Hint(Mode):

    def __init__(self, 
                 app,
                 listen_leader='f',
                 show_statusbar=True,
                 delisten_on_exec=True,
                 ):

        super().__init__(app, 
                         listen_leader=listen_leader,
                         show_statusbar=show_statusbar,
                         delisten_on_exec=delisten_on_exec,
                         )

        self.hints=None

    def activateCheck(self, event):

        leaderPressed=super().activateCheck(event)
        if leaderPressed:
            return self.app.modes.normal.listening
