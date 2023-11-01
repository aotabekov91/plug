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
        super().__init__(
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

    def getView(self):
        return self.display.currentView()

    def on_escapePressed(self):

        v=self.getView()
        if v: 
            v.select()
            v.update()

    @register(key='tc')
    def toggleCursor(self):
        self.cursor_visible=not self.cursor_visible

    @register(key='tb')
    def toggleStatusbar(self):

        bar=self.app.window.bar
        if bar.isVisible():
            bar.hide()
        else:
            bar.show()

    @register(key='gg')
    def viewGotoFirst(self):

        v=self.getView()
        if v: v.gotoFirst()
            
    @register(key='G')
    def viewGoto(self, digit=None):

        v=self.getView()
        if v: v.goto(digit)

    @register(key=']')
    def viewNext(self, digit=1): 

        v=self.getView()
        if v: 
            for d in range(digit): 
                v.next()
    
    @register(key='[')
    def viewPrev(self, digit=1): 

        view=self.getView()
        if view:
            for d in range(digit): 
                view.prev()

    @register(key=['k'])
    def viewUp(self, digit=1): 

        v=self.getView()
        if v: v.up(digit)

    @register(key='j')
    def viewDown(self, digit=1): 

        v=self.getView()
        if v: v.down(digit)

    @register(key='h')
    def viewLeft(self, digit=1): 

        v=self.getView()
        if v: v.left(digit)

    @register(key='l')
    def viewRight(self, digit=1): 

        v=self.getView()
        if v: v.right(digit)

    @register(key='zi')
    def viewZoomIn(self, digit=1): 
        
        v=self.getView()
        if v: v.zoomIn(digit)

    @register(key='zo')
    def viewZoomOut(self, digit=1): 
        
        v=self.getView()
        if v: v.zoomOut(digit)

    @register(key='K')
    def viewScreenUp(self, digit=1): 

        v=self.getView()
        if v: v.screenUp(digit)
        
    @register(key='H')
    def viewScreenLeft(self, digit=1): 

        v=self.getView()
        if v: v.screenLeft(digit)

    @register(key='J')
    def viewScreenDown(self, digit=1): 
        
        v=self.getView()
        if v: v.screenDown(digit)
        
    @register(key='L')
    def viewScreenRight(self, digit=1): 

        v=self.getView()
        if v: v.screenRight(digit)

    @register(key='r')
    def viewReadjust(self): 

        v=self.getView()
        if v: v.readjust()

    @register(key='S')
    def viewSave(self): 

        v=self.getView()
        if v: v.save()

    @register(key='c')
    def toggleContinuousMode(self): 

        v=self.getView()
        if v: v.toggleContinuousMode()

    @register('C')
    def cleanUp(self): 

        v=self.getView()
        if v: v.cleanUp()
        
    @register(key='w')
    def fitToWindowWidth(self): 

        v=self.getView()
        if v: v.fitToWindowWidth()

    @register(key='s')
    def fitToWindowHeight(self): 

        v=self.getView()
        if v: v.fitToWindowHeight()

    @register(key='d')
    def viewCloseCurrent(self): 
        self.display.closeView()

    @register(key='<c-w>v')
    def displaySplitVertical(self): 

        if self.getView():
            self.display.split(True)

    @register(key='<c-w>s') 
    def displaySplitHorizontal(self):

        if self.getView():
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

    @register(key='<c-d>f', modes=['command'])
    def dockToggleFullscreen(self): 
        self.app.window.docks.toggleFullscreen()

    @register(key='<c-d>zi', modes=['command'])
    def dockZoomIn(self, digit=1): 
        self.app.window.docks.zoomIn(digit)
        
    @register(key='<c-d>zo', modes=['command'])
    def dockZoomOut(self, digit=1): 
        self.app.window.docks.zoomOut(digit)

    @register(key='<c-d>k', modes=['command'])
    def dockUp(self): 
        self.app.window.docks.goto('up')

    @register(key='<c-d>j', modes=['command'])
    def dockDown(self): 
        self.app.window.docks.goto('down')

    @register(key='<c-d>h', modes=['command'])
    def dockLeft(self): 
        self.app.window.docks.goto('left')

    @register(key='<c-d>l', modes=['command'])
    def dockRight(self): 
        self.app.window.docks.goto('right')

    @register('<c-d>K', modes=['command'])
    def dockMoveUp(self): 
        self.app.window.docks.move('up')

    @register('<c-d>J', modes=['command'])
    def dockMoveDown(self): 
        self.app.window.docks.move('down')

    @register('<c-d>H', modes=['command'])
    def dockMoveLeft(self): 
        self.app.window.docks.move('left')

    @register('<c-d>L', modes=['command'])
    def dockMoveRight(self): 
        self.app.window.docks.move('right')

    @register(key='<c-d>d', modes=['command'])
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

    @register(key='yy')
    def yank(self):

        v=self.getView()
        if v:
            yank=getattr(v, 'yank', None)
            if yank: yank()
