from PyQt5 import QtCore
from plug.qt import Plug
from gizmo.utils import tag

class Normal(Plug):

    name='normal'
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

    def listen(self):

        super().listen()
        v=self.getView()
        if v: v.setFocus()

    def getView(self):
        return self.display.currentView()

    def cleanUp(self):

        v=self.getView()
        if v: v.redraw()

    @tag(key='tc')
    def toggleCursor(self):
        
        v=not self.cursor_visible
        self.cursor_visible=v

    @tag(key='tb')
    def toggleStatusbar(self):

        bar=self.app.window.bar
        if bar.isVisible():
            bar.hide()
        else:
            bar.show()

    @tag(key='gg')
    def viewGotoFirst(self):

        v=self.getView()
        if v: v.gotoFirst()
            
    @tag(key='G')
    def viewGoto(self, digit=None):

        v=self.getView()
        if v: 
            if digit is None:
                v.gotoLast()
            else:
                v.goto(digit)

    @tag(key='n')
    def viewNextItem(self, digit=1): 

        v=self.getView()
        if v and v.check('hasLayout'): 
            v.nextItem(digit)
    
    @tag(key='p')
    def viewPrevItem(self, digit=1): 

        v=self.getView()
        if v and v.check('hasLayout'): 
            v.prevItem(digit)

    @tag(key=['k'])
    def viewUp(self, digit=1): 

        v=self.getView()
        if v and v.check('canMove'): 
            v.up(digit)

    @tag(key='j')
    def viewDown(self, digit=1): 

        v=self.getView()
        if v and v.check('canMove'):
            v.down(digit)

    @tag(key='h')
    def viewLeft(self, digit=1): 

        v=self.getView()
        if v and v.check('canMove'): 
            v.left(digit)

    @tag(key='l')
    def viewRight(self, digit=1): 

        v=self.getView()
        if v and v.check('canMove'): 
            v.right(digit)

    @tag(key='zi')
    def viewZoomIn(self, digit=1): 
        
        v=self.getView()
        if v and v.check('canZoom'): 
            v.zoomIn(digit)

    @tag(key='zo')
    def viewZoomOut(self, digit=1): 
        
        v=self.getView()
        if v and v.check('canZoom'): 
            v.zoomOut(digit)

    @tag(key='K')
    def viewScreenUp(self, digit=1): 

        v=self.getView()
        if v and v.check('canMove'): 
            v.screenUp(digit)
        
    @tag(key='H')
    def viewScreenLeft(self, digit=1): 

        v=self.getView()
        if v and v.check('canMove'): 
            v.screenLeft(digit)

    @tag(key='J')
    def viewScreenDown(self, digit=1): 
        
        v=self.getView()
        if v and v.check('canMove'): 
            v.screenDown(digit)
        
    @tag(key='L')
    def viewScreenRight(self, digit=1): 

        v=self.getView()
        if v and v.check('canMove'): 
            v.screenRight(digit)

    @tag(key='r')
    def viewReadjust(self): 

        v=self.getView()
        if v: v.readjust()

    @tag(key='S')
    def viewSave(self): 

        v=self.getView()
        if v: v.save()

    @tag(key='c')
    def toggleContinuousMode(self): 

        v=self.getView()
        if v: v.toggleContinuousMode()

    @tag('C')
    def cleanUp(self): 

        v=self.getView()
        if v: v.cleanUp()
        
    @tag(key='w')
    def fitToWidth(self): 

        v=self.getView()
        if v and hasattr(v, 'canFit'): 
            v.fitToWidth()

    @tag(key='s')
    def fitToHeight(self): 

        v=self.getView()
        if v and hasattr(v, 'canFit'): 
            v.fitToHeight()

    @tag(key='d')
    def viewCloseCurrent(self): 
        self.display.closeView()

    @tag(key='<c-w>v')
    def displaySplitVertical(self): 

        if self.getView():
            self.display.split(True)

    @tag(key='<c-w>s') 
    def displaySplitHorizontal(self):

        if self.getView():
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

    @tag(key='<c-d>f', modes=['command'])
    def dockToggleFullscreen(self): 
        self.app.window.docks.toggleFullscreen()

    @tag(key='<c-d>zi', modes=['command'])
    def dockZoomIn(self, digit=1): 
        self.app.window.docks.zoomIn(digit)
        
    @tag(key='<c-d>zo', modes=['command'])
    def dockZoomOut(self, digit=1): 
        self.app.window.docks.zoomOut(digit)

    @tag(key='<c-d>k', modes=['command'])
    def dockUp(self): 
        self.app.window.docks.goto('up')

    @tag(key='<c-d>j', modes=['command'])
    def dockDown(self): 
        self.app.window.docks.goto('down')

    @tag(key='<c-d>h', modes=['command'])
    def dockLeft(self): 
        self.app.window.docks.goto('left')

    @tag(key='<c-d>l', modes=['command'])
    def dockRight(self): 
        self.app.window.docks.goto('right')

    @tag('<c-d>K', modes=['command'])
    def dockMoveUp(self): 
        self.app.window.docks.move('up')

    @tag('<c-d>J', modes=['command'])
    def dockMoveDown(self): 
        self.app.window.docks.move('down')

    @tag('<c-d>H', modes=['command'])
    def dockMoveLeft(self): 
        self.app.window.docks.move('left')

    @tag('<c-d>L', modes=['command'])
    def dockMoveRight(self): 
        self.app.window.docks.move('right')

    @tag(key='<c-d>d', modes=['command'])
    def dockHideAll(self): 
        self.app.window.docks.hideAll()

    @tag('<c-q>', modes=['any'])
    def quit(self):
        self.app.deactivate()

    @tag('fi')
    def incrementFold(self): 
        self.display.incrementFold()

    @tag('fd')
    def decrementFold(self): 
        self.display.decrementFold()

    @tag(key='yy')
    def yank(self):

        v=self.getView()
        if v:
            yank=getattr(v, 'yank', None)
            if yank: yank()
