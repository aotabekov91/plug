from plug.qt import Plug
from gizmo.utils import tag

class Move(Plug):

    def __init__(
            self, 
            name='move',
            leader_keys={
                'command': 'm',
                'Move': '<c-.>',
                },
            **kwargs
            ):

        super().__init__(
                name=name, 
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

    @tag('h')
    def moveLeft(self, digit=1):

        for d in range(digit):
            self.move('left', 'move')

    @tag('l')
    def moveRight(self, digit=1):
        
        for d in range(digit):
            self.move('right', 'move')

    @tag('k')
    def moveUp(self, digit=1):

        for d in range(digit):
            self.move('up', 'move')

    @tag('j')
    def moveDown(self, digit=1):

        for d in range(digit):
            self.move('down', 'move')

    @tag('H')
    def repositionLeft(self, digit=1):

        for d in range(digit):
            self.move('left', 'reposition')

    @tag('L')
    def repositionRight(self, digit=1):
        
        for d in range(digit):
            self.move('right', 'reposition')

    @tag('K')
    def repositionUp(self, digit=1):

        for d in range(digit):
            self.move('up', 'reposition')

    @tag('J')
    def repositionDown(self, digit=1):

        for d in range(digit):
            self.move('down', 'reposition')
