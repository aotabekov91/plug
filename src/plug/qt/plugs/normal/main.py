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

    @register(key='tc')
    def toggleCursor(self):
        self.cursor_visible=not self.cursor_visible

    @register(key='gg')
    def viewGotoFirst(self):

        v=self.currentView()
        if v: v.gotoFirst()
            
    @register(key='G')
    def viewGoto(self, digit=None):

        v=self.currentView()
        if v: v.goto(digit)

    @register(key=']')
    def viewNext(self, digit=1): 

        v=self.currentView()
        if v: 
            for d in range(digit): 
                v.next()
    
    @register(key='[')
    def viewPrev(self, digit=1): 

        view=self.currentView()
        if view:
            for d in range(digit): 
                view.prev()

    @register(key=['k'])
    def viewUp(self, digit=1): 

        v=self.currentView()
        if v: v.up(digit)

    @register(key='j')
    def viewDown(self, digit=1): 

        v=self.currentView()
        if v: v.down(digit)

    @register(key='h')
    def viewLeft(self, digit=1): 

        v=self.currentView()
        if v: v.left(digit)

    @register(key='l')
    def viewRight(self, digit=1): 

        v=self.currentView()
        if v: v.right(digit)

    @register(key='zi')
    def viewZoomIn(self, digit=1): 
        
        v=self.currentView()
        if v: v.zoomIn(digit)

    @register(key='zo')
    def viewZoomOut(self, digit=1): 
        
        v=self.currentView()
        if v: v.zoomOut(digit)

    @register(key='K')
    def viewPageUp(self, digit=1): 

        v=self.currentView()
        if v: v.pageUp(digit)

    @register(key='J')
    def viewPageDown(self, digit=1): 
        
        v=self.currentView()
        if v: v.pageDown(digit)

    @register(key='r')
    def viewReadjust(self): 

        v=self.currentView()
        if v: v.readjust()

    @register(key='S')
    def viewSave(self): 

        v=self.currentView()
        if v: v.save()

    @register(key='d')
    def viewCloseCurrent(self): 
        self.display.closeView()

    @register(key='<c-w>v')
    def displaySplitVertical(self): 

        if self.currentView():
            self.display.split(True)

    @register(key='<c-w>s') 
    def displaySplitHorizontal(self):

        if self.currentView():
            self.display.split(False)

    @register('<c-w>K')
    def displayMoveUp(self): 
        self.display.move('up')

    @register('<c-w>J')
    def displayMoveDown(self): 
        self.display.move('down')

    @register('<c-w>H')
    def displayMoveLeft(self): 
        self.display.move('left')

    @register('<c-w>L')
    def displayMoveRight(self): 
        self.display.move('right')

    @register('<c-w>k')
    def displayUp(self): 
        self.display.goto('up')

    @register('<c-w>j')
    def displayDown(self): 
        self.display.goto('down')

    @register('<c-w>l')
    def displayRight(self): 
        self.display.goto('right')

    @register('<c-w>h')
    def displayLeft(self): 
        self.display.goto('left')

    @register('<c-w>gg')
    def displayGotoFirst(self): 
        self.display.goto('first')

    @register('<c-w>G')
    def displayGoto(self, digit=None): 
        self.display.goto('last', digit)

    @register('<c-w>n')
    def displayNext(self): 
        self.display.goto('next')

    @register('<c-w>p')
    def displayPrev(self): 
        self.display.goto('prev')

    @register('<c-w>f')
    def displayToggleFullscreen(self): 
        self.display.toggleFullscreen()

    @register(key='<c-w>df', modes=['any'])
    def dockToggleFullscreen(self): 
        self.app.window.docks.toggleFullscreen()

    @register(key='<c-w>dzi', modes=['any'])
    def dockZoomIn(self, digit=1): 
        self.app.window.docks.zoomIn(digit)
        
    @register(key='<c-w>dzo', modes=['any'])
    def dockZoomOut(self, digit=1): 
        self.app.window.docks.zoomOut(digit)

    @register(key='<c-w>dk', modes=['any'])
    def dockUp(self): 
        self.app.window.docks.goto('top')

    @register(key='<c-w>dj', modes=['any'])
    def dockDown(self): 
        self.app.window.docks.goto('bottom')

    @register(key='<c-w>dh', modes=['any'])
    def dockLeft(self): 
        self.app.window.docks.goto('left')

    @register(key='<c-w>dl', modes=['any'])
    def dockRight(self): 
        self.app.window.docks.goto('right')

    @register(key='<c-w>dd', modes=['any'])
    def dockHideAll(self): 
        self.app.window.docks.hideAll()

    @register('<c-q>', modes=['any'])
    def quit(self):
        self.app.exit()

    @register('fi')
    def incrementFold(self): 
        self.display.incrementFold()

    @register('fd')
    def decrementFold(self): 
        self.display.decrementFold()
