from plug.qt import Plug
from gizmo.utils import tag

class Normal(Plug):

    isMode=True
    name='normal'
    cursor_visible=False
    delisten_on_exec=False

    def setup(self):

        super().setup()
        self.m_uiman=self.app.uiman

    def octivate(self):

        super().octivate()
        v=self.app.handler.view()
        if v: v.cleanUp()

    def getDefaultView(self):
        return self.app.display.currentView()

    def go(self, *args, **kwargs):

        v=self.app.handler.view()
        if v and v.check('canGo'):
            v.go(*args, **kwargs)

    @tag('tc')
    def toggleCursor(self):
        
        v=not self.cursor_visible
        self.cursor_visible=v

    @tag('tb')
    def toggleStatusbar(self):
        self.app.m_uiman.bar.toggle()

    @tag('gg')
    def gotoFirst(self):
        self.go(kind='first')

    @tag('G')
    def goto(self, digit=None):
        self.go(digit=digit)

    @tag('n')
    def gotoNext(self, digit=1): 
        self.go(kind='next', digit=digit)

    @tag('p')
    def gotoPrev(self, digit=1): 
        self.go(kind='prev', digit=digit)

    @tag('k')
    def up(self, digit=1): 
        self.go(kind='up', digit=digit)

    @tag('j')
    def down(self, digit=1): 
        self.go(kind='down', digit=digit)

    @tag('h')
    def left(self, digit=1): 
        self.go(kind='left', digit=digit)

    @tag('l')
    def right(self, digit=1): 
        self.go(kind='right', digit=digit)

    @tag('zi')
    def zoomIn(self, digit=1): 
        self.m_uiman.scale(kind='in', digit=digit)

    @tag('zo')
    def zoomOut(self, digit=1): 
        self.m_uiman.scale(kind='out', digit=digit)

    @tag('zw')
    def zoomToWidth(self): 
        self.m_uiman.scale(kind='width')

    @tag('zh')
    def zoomToHeight(self): 
        self.m_uiman.scale(kind='height')

    @tag('K')
    def screenUp(self, digit=1): 
        self.go(kind='screenUp', digit=digit)

    @tag('J')
    def screenDown(self, digit=1): 
        self.go(kind='screenDown', digit=digit)
        
    @tag('H')
    def screenLeft(self, digit=1): 
        self.go(kind='screenLeft', digit=digit)

    @tag('L')
    def screenRight(self, digit=1): 
        self.go(kind='screenRight', digit=digit)

    @tag('<c-w>c')
    def toggleContinuousMode(self): 

        v=self.app.handler.view()
        if v and v.check('canFlow'): 
            v.toggleContinuousMode()

    @tag('<c-w>v')
    def splitVertically(self): 
        self.m_uiman.split(kind='vertical')

    @tag('<c-w>s') 
    def splitHorizontally(self):
        self.m_uiman.split(kind='horizontal')

    @tag('<c-w>K')
    def moveViewUp(self): 
        self.m_uiman.move(kind='up')

    @tag('<c-w>J')
    def moveViewDown(self): 
        self.m_uiman.move(kind='down')

    @tag('<c-w>H')
    def moveViewLeft(self): 
        self.m_uiman.move(kind='left')

    @tag('<c-w>L')
    def moveViewRight(self): 
        self.m_uiman.move(kind='right')

    @tag('<c-w>k')
    def upView(self): 
        self.m_uiman.goto(kind='up')

    @tag('<c-w>j')
    def downView(self): 
        self.m_uiman.goto(kind='down')

    @tag('<c-w>l')
    def rightView(self): 
        self.m_uiman.goto(kind='right')

    @tag('<c-w>h')
    def leftView(self): 
        self.m_uiman.goto(kind='left')

    @tag('<c-w>gg')
    def gotoFirstView(self): 
        self.m_uiman.goto(kind='first')

    @tag('<c-w>G')
    def gotoView(self, digit=None): 
        self.m_uiman.goto(kind='last', digit=digit)

    @tag('<c-w>n')
    def gotoNextView(self, digit=1): 
        self.m_uiman.goto(kind='next', digit=digit)

    @tag('<c-w>p')
    def gotoPrevView(self, digit=1): 
        self.m_uiman.goto(kind='prev', digit=digit)

    @tag('<c-d>H')
    def hideAllDocks(self): 
        self.app.m_uiman.docks.hideAll()

    @tag('f')
    def toggleFullscreen(self): 
        self.m_uiman.toggleFullscreen(kind='app')

    @tag('<c-w>f')
    def toggleFullscreenView(self): 

        raise
        self.m_uiman.toggleFullscreen()

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
