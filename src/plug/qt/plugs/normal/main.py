from PyQt5 import QtCore
from plug.qt import Plug
from gizmo.utils import tag

class Normal(Plug):

    name='normal'
    isMode=True
    hasView=True
    listen_leader='@'
    cursor_visible=False
    delisten_on_exec=False
    escapePressed=QtCore.pyqtSignal()

    def setup(self):

        super().setup()
        self.display=self.app.display
        self.escapePressed.connect(
                self.cleanUp)

    def view(self):
        return self.app.handler.view()

    def getDefaultView(self):
        return self.app.display.currentView()

    def cleanUp(self): 

        v=self.view()
        if v: v.cleanUp()

    @tag('tc')
    def toggleCursor(self):
        
        v=not self.cursor_visible
        self.cursor_visible=v

    @tag('tb')
    def toggleStatusbar(self):

        bar=self.app.ui.bar
        if bar.isVisible():
            bar.hide()
        else:
            bar.show()

    @tag('gg')
    def viewGotoFirst(self):

        v=self.view()
        if v and v.check('canGo'):
            v.go('first')
            
    @tag('G')
    def viewGoto(self, digit=None):

        v=self.view()
        if v and v.check('canGo'): 
            v.go(digit or 'last')

    @tag('n')
    def viewNextItem(self, digit=1): 

        v=self.view()
        if v and v.check('canGo'): 
            v.go('next', digit=digit)
    
    @tag('p')
    def viewPrevItem(self, digit=1): 

        v=self.view()
        if v and v.check('canGo'): 
            v.go('prev', digit=digit)

    @tag('k')
    def viewUp(self, digit=1): 

        v=self.view()
        if v and v.check('canMove'): 
            v.move('up', digit)

    @tag('j')
    def viewDown(self, digit=1): 

        v=self.view()
        if v and v.check('canMove'):
            v.move('down', digit)

    @tag('h')
    def viewLeft(self, digit=1): 

        v=self.view()
        if v and v.check('canMove'): 
            v.move('left', digit)

    @tag('l')
    def viewRight(self, digit=1): 

        v=self.view()
        if v and v.check('canMove'): 
            v.move('right', digit)

    @tag('zi')
    def viewZoomIn(self, digit=1): 
        
        v=self.view()
        if v and v.check('canScale'): 
            v.scale('zoomIn', digit=digit)

    @tag('zo')
    def viewZoomOut(self, digit=1): 
        
        v=self.view()
        if v and v.check('canScale'): 
            v.scale('zoomOut', digit=digit)

    @tag('w')
    def fitToWidth(self): 

        v=self.view()
        if v and hasattr(v, 'canScale'): 
            v.scale('fitToWidth')

    @tag('s')
    def fitToHeight(self): 

        v=self.view()
        if v and hasattr(v, 'canScale'): 
            v.scale('fitToHeight')

    @tag('K')
    def viewScreenUp(self, digit=1): 

        v=self.view()
        if v and v.check('canMove'): 
            v.move('screenUp', digit)
        
    @tag('H')
    def viewScreenLeft(self, digit=1): 

        v=self.view()
        if v and v.check('canMove'): 
            v.move('screenLeft', digit)

    @tag('J')
    def viewScreenDown(self, digit=1): 
        
        v=self.view()
        if v and v.check('canMove'): 
            v.move('screenDown', digit)
        
    @tag('L')
    def viewScreenRight(self, digit=1): 

        v=self.view()
        if v and v.check('canMove'): 
            v.move('screenRight', digit)

    @tag('<c-w>c')
    def toggleContinuousMode(self): 

        v=self.view()
        if v: v.toggleContinuousMode()

    @tag('<c-w>d')
    def viewCloseCurrent(self): 
        self.display.closeView()

    @tag('<c-w>v')
    def displaySplitVertical(self): 

        if self.view():
            self.display.split(True)

    @tag('<c-w>s') 
    def displaySplitHorizontal(self):

        if self.view():
            self.display.split(False)

    @tag('<c-w>K')
    def displayMoveUp(self): 
        self.display.move('up')

    @tag('<c-w>J')
    def displayMoveDown(self): 
        self.display.move('down')

    @tag('<c-w>H')
    def displayMoveLeft(self): 
        self.display.move('left')

    @tag('<c-w>L')
    def displayMoveRight(self): 
        self.display.move('right')

    @tag('<c-w>k')
    def displayUp(self): 
        self.display.goto('up')

    @tag('<c-w>j')
    def displayDown(self): 
        self.display.goto('down')

    @tag('<c-w>l')
    def displayRight(self): 
        self.display.goto('right')

    @tag('<c-w>h')
    def displayLeft(self): 
        self.display.goto('left')

    @tag('<c-w>gg')
    def displayGotoFirst(self): 
        self.display.goto('first')

    @tag('<c-w>G')
    def displayGoto(self, digit=None): 
        self.display.goto('last', digit)

    @tag('<c-w>n')
    def displayNext(self): 
        self.display.goto('next')

    @tag('<c-w>p')
    def displayPrev(self): 
        self.display.goto('prev')

    @tag('<c-w>f')
    def displayToggleFullscreen(self): 
        self.display.toggleFullscreen()

    @tag('<c-d>f', modes=['command'])
    def dockToggleFullscreen(self): 
        self.app.ui.docks.toggleFullscreen()

    @tag('<c-d>zi', modes=['command'])
    def dockZoomIn(self, digit=1): 
        self.app.ui.docks.zoomIn(digit)
        
    @tag('<c-d>zo', modes=['command'])
    def dockZoomOut(self, digit=1): 
        self.app.ui.docks.zoomOut(digit)

    @tag('<c-d>k', modes=['command'])
    def dockUp(self): 
        self.app.ui.docks.goto('up')

    @tag('<c-d>j', modes=['command'])
    def dockDown(self): 
        self.app.ui.docks.goto('down')

    @tag('<c-d>h', modes=['command'])
    def dockLeft(self): 
        self.app.ui.docks.goto('left')

    @tag('<c-d>l', modes=['command'])
    def dockRight(self): 
        self.app.ui.docks.goto('right')

    @tag('<c-d>K', modes=['command'])
    def dockMoveUp(self): 
        self.app.ui.docks.move('up')

    @tag('<c-d>J', modes=['command'])
    def dockMoveDown(self): 
        self.app.ui.docks.move('down')

    @tag('<c-d>H', modes=['command'])
    def dockMoveLeft(self): 
        self.app.ui.docks.move('left')

    @tag('<c-d>L', modes=['command'])
    def dockMoveRight(self): 
        self.app.ui.docks.move('right')

    @tag('<c-d>d', modes=['command'])
    def dockHideAll(self): 
        self.app.ui.docks.hideAll()

    @tag('<c-q>', modes=['any'])
    def quit(self):
        self.app.deactivate()

    @tag('<c-p>', modes=['any'])
    def setDefaultView(self):
        self.app.handler.setDefaultView()

    @tag('fi')
    def incrementFold(self): 
        self.display.incrementFold()

    @tag('fd')
    def decrementFold(self): 
        self.display.decrementFold()

    @tag('yy')
    def yank(self):

        v=self.view()
        if v and v.check('canYank'):
            v.yank()
