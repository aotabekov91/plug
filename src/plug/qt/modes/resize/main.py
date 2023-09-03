from plug.qt import PlugObj
from plug.qt.utils import register

class Resize(PlugObj):

    def __init__(self, 
                 app, 
                 name='resize',
                 listen_leader='<c-r>',
                 **kwargs,
                 ):

        super(Resize, self).__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader,
                **kwargs,
                )

    def crement(self, direction, kind):

        prev=self.app.plugman.prev
        # Todo add dock resizing here also
        # bar=self.app.window.bar
        display=self.app.window.main.display

        if prev.name=='normal':
            display.resize(direction, kind)

    @register('l')
    def incrementLeft(self, digit=1):

        for d in range(digit):
            self.crement('left', 'increment')

    @register('h')
    def incrementRight(self, digit=1):
        
        for d in range(digit):
            self.crement('right', 'increment')

    @register('k')
    def incrementUp(self, digit=1):

        for d in range(digit):
            self.crement('up', 'increment')

    @register('j')
    def incrementDown(self, digit=1):

        for d in range(digit):
            self.crement('down', 'increment')

    @register('L')
    def decrmentLeft(self, digit=1):

        for d in range(digit):
            self.crement('left', 'decrment')

    @register('H')
    def decrmentRight(self, digit=1):
        
        for d in range(digit):
            self.crement('right', 'decrment')

    @register('K')
    def decrmentUp(self, digit=1):

        for d in range(digit):
            self.crement('up', 'decrment')

    @register('J')
    def decrmentDown(self, digit=1):

        for d in range(digit):
            self.crement('down', 'decrment')
