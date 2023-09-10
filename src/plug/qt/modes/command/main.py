from plug.qt import PlugObj
from plug.qt.utils import register

class Command(PlugObj):

    def __init__(self, 
                 app, 
                 name='command',
                 show_statusbar=True, 
                 listen_leader='<c-,>',
                 delisten_on_exec=True,
                 **kwargs,
                 ):

        super(Command, self).__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader,
                show_statusbar=show_statusbar, 
                delisten_on_exec=delisten_on_exec,
                **kwargs,
                )

    @register('<c-q>', modes=['any'])
    def exit(self):

        if self.app: self.app.exit()
