from plug.qt import Plug

class Visual(Plug):

    def __init__(self, 
                 *args,
                 name='visual',
                 show_statusbar=True,
                 listen_leader='<c-V>',
                 **kwargs,
                 ):

        self.hints=None
        self.hinting=False

        super().__init__(
                *args,
                name=name, 
                listen_leader=listen_leader, 
                show_statusbar=show_statusbar, 
                **kwargs
                )

    def delisten(self):

        super().delisten()
        self.hints=False
        if self.hinting:
            self.app.display.view.update()
        self.hinting=False

    def listen(self):

        super().listen()
        self.app.window.main.setFocus()
