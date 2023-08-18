from .base import Mode
from plug.qt.utils  import register

class Normal(Mode):

    def __init__(self, 
                 app=None,
                 name='normal',
                 listen_leader='@',
                 delisten_on_exec=False,
                 **kwargs,
                 ):

        super(Normal, self).__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader,
                delisten_on_exec=delisten_on_exec, 
                **kwargs,)

    def listen(self):

        super().listen()
        self.app.main.setFocus()

    def incrementUp(self, digit=1): 

        if self.view:
            for d in range(digit): self.view.incrementUp()

    def incrementDown(self, digit=1): 

        if self.view:
            for d in range(digit): self.view.incrementDown()

    def incrementLeft(self, digit=1): 

        if self.view:
            for d in range(digit): self.view.incrementLeft()

    def incrementRight(self, digit=1): 

        if self.view:
            for d in range(digit): self.view.incrementRight()

    @register(key='G')
    def gotoEnd(self):

        view=self.app.main.display.view
        if view: view.gotoEnd()

    @register(key='gg')
    def gotoBegin(self):

        view=self.app.main.display.view
        if view: view.gotoBegin()

    @register(key=']')
    def next(self, digit=1): 

        view=self.app.main.display.view
        if view: 
            for d in range(digit): view.next()
    
    @register(key='[')
    def prev(self, digit=1): 

        view=self.app.main.display.view
        if view:
            for d in range(digit): view.prev()

    @register(key='k')
    def up(self, digit=1): 

        view=self.app.main.display.view
        if view: 
            for d in range(digit): view.up()

    @register(key='j')
    def down(self, digit=1): 

        view=self.app.main.display.view
        if view: 
            for d in range(digit): view.down()

    @register(key='h')
    def left(self, digit=1): 

        view=self.app.main.display.view
        if view: 
            for d in range(digit): view.left()

    @register(key='l')
    def right(self, digit=1): 

        view=self.app.main.display.view
        if view: 
            for d in range(digit): view.right()

    @register(key='zi')
    def zoomIn(self, digit=1): 
        
        view=self.app.main.display.view
        if view:
            for d in range(digit): view.zoomIn()

    @register(key='zo')
    def zoomOut(self, digit=1): 
        
        view=self.app.main.display.view
        if view:
            for d in range(digit): view.zoomOut()

    @register(key='g')
    def gotoPage(self, digit=1):

        view=self.app.main.display.view
        if view: view.goto(digit)

    @register(key='K')
    def pageUp(self, digit=1): 

        view=self.app.main.display.view
        if view:
            for d in range(digit): view.pageUp()

    @register(key='J')
    def pageDown(self, digit=1): 
        
        view=self.app.main.display.view
        if view:
            for d in range(digit): view.pageDown()

    @register(key='r')
    def readjust(self): 

        view=self.app.main.display.view
        if view: view.readjust()

    @register(key='S')
    def save(self): 

        view=self.app.main.display.view
        if view: view.save()

    @register('fc')
    def focusCurrentView(self): 

        self.app.main.display.focusCurrentView()

    @register(key='fx')
    def closeCurrentView(self): 

        self.app.main.display.closeView()

    @register('fk')
    def focusUpView(self): 

        self.app.main.display.focus(-1)

    @register('fj')
    def focusDownView(self): 

        self.app.main.display.focus(+1)

    @register('fi')
    def incrementFold(self): 

        self.app.main.display.incrementFold()

    @register('fd')
    def decrementFold(self): 

        self.app.main.display.decrementFold()

    @register(key='tc', modes=['normal', 'command'])
    def toggleCursor(self): 

        self.app.main.display.toggleCursor()
