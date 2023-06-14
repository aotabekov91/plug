from ..base import Mode 

class Visual(Mode):

    def __init__(self, app):

        super().__init__(app, 
                         listen_leader='#',
                         show_statusbar=True,
                         delisten_on_exec=False,
                         )

        self.hints=None
        self.hinting=False
