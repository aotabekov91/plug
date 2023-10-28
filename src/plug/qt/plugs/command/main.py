from plug.qt import Plug

class Command(Plug):

    def __init__(self, 
                 app, 
                 name='command',
                 show_statusbar=True, 
                 listen_leader='<c-,>',
                 delisten_on_exec=True,
                 **kwargs,
                 ):

        self.client=None
        super().__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader,
                show_statusbar=show_statusbar, 
                delisten_on_exec=delisten_on_exec,
                **kwargs,
                )
        self.app.moder.modeIsToBeSet.connect(
                self.setClient)

    def setClient(self, mode):

        if mode==self:
            self.client=self.app.moder.prev
