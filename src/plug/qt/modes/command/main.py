from .base import Mode

class Command(Mode):

    def __init__(self, 
                 app, 
                 name='command',
                 show_statusbar=True, 
                 listen_leader='Ctrl+,',
                 **kwargs,
                 ):

        super(Command, self).__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader,
                show_statusbar=show_statusbar, 
                **kwargs,
                )
