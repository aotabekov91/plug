from plug.qt import Plug
from gizmo.utils import tag

class Resize(Plug):

    def __init__(self, 
                 app, 
                 name='resize',
                 listen_leader='<c-R>',
                 **kwargs,
                 ):

        super(Resize, self).__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader,
                **kwargs,
                )

    def crement(self, direction, kind):

        prev=self.app.moder.prev
        # Todo add dock resizing here also
        # bar=self.app.ui.bar
        display=self.app.display

        if prev.name=='normal':
            display.resize(direction, kind)

    @tag('h')
    def incrementLeft(self, digit=1):

        for d in range(digit):
            self.crement('left', 'increment')

    @tag('l')
    def incrementRight(self, digit=1):
        
        for d in range(digit):
            self.crement('right', 'increment')

    @tag('k')
    def incrementUp(self, digit=1):

        for d in range(digit):
            self.crement('up', 'increment')

    @tag('j')
    def incrementDown(self, digit=1):

        for d in range(digit):
            self.crement('down', 'increment')

    @tag('H')
    def decrmentLeft(self, digit=1):

        for d in range(digit):
            self.crement('left', 'decrment')

    @tag('L')
    def decrmentRight(self, digit=1):
        
        for d in range(digit):
            self.crement('right', 'decrment')

    @tag('K')
    def decrmentUp(self, digit=1):

        for d in range(digit):
            self.crement('up', 'decrment')

    @tag('J')
    def decrmentDown(self, digit=1):

        for d in range(digit):
            self.crement('down', 'decrment')
