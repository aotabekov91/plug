from plug.qt import PlugObj

class Visual(PlugObj):

    def __init__(self, 
                 app=None,
                 name='visual',
                 show_statusbar=True,
                 listen_leader='Ctrl+v',
                 delisten_on_exec=False,
                 **kwargs,
                 ):

        self.hints=None
        self.hinting=False

        super().__init__(app=app, 
                         name=name,
                         listen_leader=listen_leader,
                         show_statusbar=show_statusbar,
                         delisten_on_exec=delisten_on_exec, 
                         **kwargs,
                         )

    def delisten(self):

        super().delisten()
        self.hints=False
        if self.hinting:
            self.app.window.main.display.view.update()
        self.hinting=False

    def listen(self):

        super().listen()
        self.app.window.main.setFocus()
