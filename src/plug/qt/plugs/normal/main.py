from plug.qt import Plug
from gizmo.utils import tag

class Normal(Plug):

    isMode=True
    name='normal'
    cursor_visible=False
    delisten_on_exec=False

    def octivate(self):

        super().octivate()
        v=self.app.handler.view()
        if v: v.cleanUp()

    def getDefaultView(self):
        return self.app.display.currentView()

    @tag('tc')
    def toggleCursor(self):
        
        v=not self.cursor_visible
        self.cursor_visible=v

    @tag('tb')
    def toggleStatusbar(self):
        self.app.ui.bar.toggle()

    @tag('gg')
    def gotoFirst(self):

        v=self.app.handler.view()
        if v and v.check('canGo'):
            v.go('first')
            
    @tag('G')
    def goto(self, digit=None):

        v=self.app.handler.view()
        if v and v.check('canGo'): 
            if digit is None:
                v.go('last')
            else:
                v.go(digit=digit)

    @tag('n')
    def gotoNext(self, digit=1): 

        v=self.app.handler.view()
        if v and v.check('canGo'): 
            v.go('next', digit=digit)
    
    @tag('p')
    def gotoPrev(self, digit=1): 

        v=self.app.handler.view()
        if v and v.check('canGo'): 
            v.go('prev', digit=digit)

    @tag('k')
    def up(self, digit=1): 

        v=self.app.handler.view()
        if v and v.check('canGo'): 
            v.go('up', digit)

    @tag('j')
    def down(self, digit=1): 

        v=self.app.handler.view()
        if v and v.check('canGo'):
            v.go('down', digit)

    @tag('h')
    def left(self, digit=1): 

        v=self.app.handler.view()
        if v and v.check('canGo'): 
            v.go('left', digit)

    @tag('l')
    def right(self, digit=1): 

        v=self.app.handler.view()
        if v and v.check('canGo'): 
            v.go('right', digit)

    @tag('zi')
    def zoomIn(self, digit=1): 

        self.app.uiman.scale(
                kind='in', digit=digit)

    @tag('zo')
    def zoomOut(self, digit=1): 
        
        self.app.uiman.scale(
                kind='out', digit=digit)

    @tag('zw')
    def zoomToWidth(self): 
        
        self.app.uiman.scale(
                kind='width')

    @tag('zh')
    def zoomToHeight(self): 

        self.app.uiman.scale(
                kind='height')

    @tag('K')
    def screenUp(self, digit=1): 

        v=self.app.handler.view()
        if v and v.check('canGo'): 
            v.go('screenUp', digit)

    @tag('J')
    def screenDown(self, digit=1): 
        
        v=self.app.handler.view()
        if v and v.check('canGo'): 
            v.go('screenDown', digit)
        
    @tag('H')
    def screenLeft(self, digit=1): 

        v=self.app.handler.view()
        if v and v.check('canGo'): 
            v.go('screenLeft', digit)

    @tag('L')
    def screenRight(self, digit=1): 

        v=self.app.handler.view()
        if v and v.check('canGo'): 
            v.go('screenRight', digit)

    @tag('<c-w>c')
    def toggleContinuousMode(self): 

        v=self.app.handler.view()
        if v and v.check('canFlow'): 
            v.toggleContinuousMode()

    @tag('<c-w>v')
    def splitVertically(self): 
        self.app.uiman.split(kind='vertical')

    @tag('<c-w>s') 
    def splitHorizontally(self):
        self.app.uiman.split(kind='horizontal')

    @tag('<c-w>K')
    def moveViewUp(self): 
        self.app.uiman.move(kind='up')

    @tag('<c-w>J')
    def moveViewDown(self): 
        self.app.uiman.move(kind='down')

    @tag('<c-w>H')
    def moveViewLeft(self): 
        self.app.uiman.move(kind='left')

    @tag('<c-w>L')
    def moveViewRight(self): 
        self.app.uiman.move(kind='right')

    @tag('<c-w>k')
    def upView(self): 
        self.app.uiman.goto(kind='up')

    @tag('<c-w>j')
    def downView(self): 
        self.app.uiman.goto(kind='down')

    @tag('<c-w>l')
    def rightView(self): 
        self.app.uiman.goto(kind='right')

    @tag('<c-w>h')
    def leftView(self): 
        self.app.uiman.goto(kind='left')

    @tag('<c-w>gg')
    def gotoFirstView(self): 
        self.app.uiman.goto(kind='first')

    @tag('<c-w>G')
    def gotoView(self, digit=None): 

        self.app.uiman.goto(
                kind='last', digit=digit)

    @tag('<c-w>n')
    def gotoNextView(self, digit=1): 

        self.app.uiman.goto(
                kind='next', digit=digit)

    @tag('<c-w>p')
    def gotoPrevView(self, digit=1): 

        self.app.uiman.goto(
                kind='prev', digit=digit)

    @tag('<c-d>H')
    def hideAllDocks(self): 
        self.app.ui.docks.hideAll()

    @tag('f')
    def toggleFullscreen(self): 

        self.app.uiman.toggleFullscreen(
                kind='app')

    @tag('<c-w>f')
    def toggleFullscreenView(self): 

        raise
        self.app.uiman.toggleFullscreen()

    @tag('yy')
    def yank(self):

        raise
        v=self.app.handler.view()
        if v and v.check('canYank'):
            v.yank()

    @tag('<c-q>', modes=['any'])
    def quit(self):
        self.app.octivate()

    @tag('<c-p>', modes=['any'])
    def setDefaultView(self):
        self.app.handler.setDefaultView()
