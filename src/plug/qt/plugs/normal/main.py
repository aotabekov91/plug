from PyQt5 import QtGui, QtCore

from plug.qt import Plug
from gizmo.utils import register

class Normal(Plug):

    special=[
            'escape',
            'escape_bracket'
            ]

    def __init__(
            self, 
            app=None, 
            name='normal',
            special=special, 
            listen_leader='@', 
            delisten_on_exec=False,
            **kwargs
            ):

        self.cursor_visible=False
        super(Normal, self).__init__(
                app=app, 
                name=name,
                special=special,
                listen_leader=listen_leader,
                delisten_on_exec=delisten_on_exec, 
                **kwargs)

    def setup(self):

        super().setup()
        self.display=self.app.display
        self.ear.escapePressed.connect(
                self.on_escapePressed)

    def currentView(self):
        return self.display.currentView()

    def on_escapePressed(self):

        v=self.currentView()
        if v: 
            v.select()
            v.update()

    def incrementUp(self, digit=1): 

        view=self.currentView()
        if view:
            for d in range(digit): 
                view.incrementUp()

    def incrementDown(self, digit=1): 

        view=self.currentView()
        if view:
            for d in range(digit): 
                view.incrementDown()

    def incrementLeft(self, digit=1): 

        view=self.currentView()
        if view:
            for d in range(digit): 
                view.incrementLeft()

    def incrementRight(self, digit=1): 

        view=self.currentView()
        if view:
            for d in range(digit): 
                view.incrementRight()

    def gotoEnd(self):

        view=self.currentView()
        if view: view.gotoEnd()

    @register(key='gg')
    def gotoBegin(self):

        view=self.currentView()
        if view: view.gotoBegin()
            
    @register(key='G')
    def goto(self, digit=None):

        view=self.currentView()
        if view: 
            if not digit:
                self.gotoEnd()
            else:
                view.goto(digit)

    @register(key=']')
    def next(self, digit=1): 

        view=self.currentView()
        if view: 
            for d in range(digit): 
                view.next()
    
    @register(key='[')
    def prev(self, digit=1): 

        view=self.currentView()
        if view:
            for d in range(digit): 
                view.prev()

    @register(key=['k'])
    def up(self, digit=1): 

        view=self.currentView()
        if view: 
            for d in range(digit): 
                view.up()

    @register(key='j')
    def down(self, digit=1): 

        view=self.currentView()
        if view: 
            for d in range(digit): 
                view.down()

    @register(key='h')
    def left(self, digit=1): 

        view=self.currentView()
        if view: 
            for d in range(digit): 
                view.left()

    @register(key='l')
    def right(self, digit=1): 

        view=self.currentView()
        if view: 
            for d in range(digit): 
                view.right()

    @register(key='zi')
    def zoomIn(self, digit=1): 
        
        view=self.currentView()
        if view:
            for d in range(digit): 
                view.zoomIn()

    @register(key='zo')
    def zoomOut(self, digit=1): 
        
        view=self.currentView()
        if view:
            for d in range(digit): 
                view.zoomOut()

    @register(key='K')
    def pageUp(self, digit=1): 

        view=self.currentView()
        if view:
            for d in range(digit): 
                view.pageUp()

    @register(key='J')
    def pageDown(self, digit=1): 
        
        view=self.currentView()
        if view:
            for d in range(digit): 
                view.pageDown()

    @register(key='r')
    def readjust(self): 

        view=self.currentView()
        if view: 
            view.readjust()

    @register(key='S')
    def save(self): 

        view=self.currentView()
        if view: 
            view.save()

    @register(key='<c-w>c')
    def closeCurrentView(self): 
        self.display.closeView()

    @register('fi')
    def incrementFold(self): 
        self.display.incrementFold()

    @register('fd')
    def decrementFold(self): 
        self.display.decrementFold()

    @register(key='<c-w>v')
    def splitVertical(self): 

        if self.currentView():
            self.display.split(True)

    @register(key='<c-w>s') 
    def splitHorizontal(self):

        if self.currentView():
            self.display.split(False)

    @register('<c-w>k')
    def focusUpView(self): 
        self.display.focus('up')

    @register('<c-w>j')
    def focusDownView(self): 
        self.display.focus('down')

    @register('<c-w>l')
    def focusLeftView(self): 
        self.display.focus('right')

    @register('<c-w>h')
    def focusRightView(self): 
        self.display.focus('left')

    @register('<c-w>gg')
    def focusFirstView(self): 
        self.display.focus('first')

    @register('<c-w>G')
    def focusLastView(self): 
        self.display.focus('last')

    @register('<c-w>n')
    def focusNextView(self): 
        self.display.focus('next')

    @register('<c-w>p')
    def focusPrevView(self): 
        self.display.focus('prev')

    @register('<c-q>', modes=['any'])
    def quit(self):
        self.app.exit()

    @register(key='tc')
    def toggleCursor(self):
        self.cursor_visible=not self.cursor_visible
