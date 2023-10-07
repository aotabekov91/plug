from plug.qt import Plug
from gizmo.utils import register

class Move(Plug):

    def __init__(self, 
                 app, 
                 name='move',
                 listen_leader='<c-m>',
                 **kwargs,
                 ):

        super(Move, self).__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader,
                **kwargs,
                )

    def move(self, direction, kind):

        prev=self.app.moder.prev
        # Todo add dock resizing here also
        # bar=self.app.window.bar
        display=self.app.display

        if prev.name=='normal':
            if kind=='move':
                display.move(direction)

    @register('h')
    def moveLeft(self, digit=1):

        for d in range(digit):
            self.move('left', 'move')

    @register('l')
    def moveRight(self, digit=1):
        
        for d in range(digit):
            self.move('right', 'move')

    @register('k')
    def moveUp(self, digit=1):

        for d in range(digit):
            self.move('up', 'move')

    @register('j')
    def moveDown(self, digit=1):

        for d in range(digit):
            self.move('down', 'move')

    @register('H')
    def repositionLeft(self, digit=1):

        for d in range(digit):
            self.move('left', 'reposition')

    @register('L')
    def repositionRight(self, digit=1):
        
        for d in range(digit):
            self.move('right', 'reposition')

    @register('K')
    def repositionUp(self, digit=1):

        for d in range(digit):
            self.move('up', 'reposition')

    @register('J')
    def repositionDown(self, digit=1):

        for d in range(digit):
            self.move('down', 'reposition')
