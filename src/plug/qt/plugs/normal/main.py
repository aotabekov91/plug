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
    def goToFirst(self):
        self.go(kind='first')

    @tag('G')
    def goTo(self, digit=None):
        self.go(digit=digit)

    @tag('n')
    def goToNext(self, digit=1): 
        self.go(kind='next', digit=digit)

    @tag('p')
    def goToPrev(self, digit=1): 
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

    @tag('<c-w>m')
    def moveView(self, digit=1): 
        self.m_uiman.move(digit=digit)

    @tag('<c-w>K')
    def moveUpView(self): 
        self.m_uiman.move(kind='up')

    @tag('<c-w>J')
    def moveDownView(self): 
        self.m_uiman.move(kind='down')

    @tag('<c-w>H')
    def moveLeftView(self): 
        self.m_uiman.move(kind='left')

    @tag('<c-w>L')
    def moveRightView(self): 
        self.m_uiman.move(kind='right')

    @tag('<c-w>k')
    def upView(self): 
        self.m_uiman.goTo(kind='up')

    @tag('<c-w>j')
    def downView(self): 
        self.m_uiman.goTo(kind='down')

    @tag('<c-w>l')
    def rightView(self): 
        self.m_uiman.goTo(kind='right')

    @tag('<c-w>h')
    def leftView(self): 
        self.m_uiman.goTo(kind='left')

    @tag('<c-w>gg')
    def goToFirstView(self): 
        self.m_uiman.goTo(kind='first')

    @tag(['gw', '<c-w>G'])
    def goToView(self, digit=None): 
        self.m_uiman.goTo(kind='last', digit=digit)

    @tag('<c-w>n')
    def goToNextView(self, digit=1): 
        self.m_uiman.goTo(kind='next', digit=digit)

    @tag('<c-w>p')
    def goToPrevView(self, digit=1): 
        self.m_uiman.goTo(kind='prev', digit=digit)

    @tag('<c-w>x')
    def closeView(self): 
        self.m_uiman.close(vkind='view')

    @tag('<c-t>t')
    def moveToTab(self, digit=1):

        self.m_uiman.move(
                vkind='tab', 
                digit=digit,
                kind='moveTo',
                )
        
    @tag('<c-t>m')
    def moveTab(self, digit=1):
        self.m_uiman.move(vkind='tab', digit=digit)

    @tag('<c-t>H')
    def moveLeftTab(self):
        self.m_uiman.move(vkind='tab', kind='left')

    @tag('<c-t>L')
    def moveRightTab(self):
        self.m_uiman.move(vkind='tab', kind='right')

    @tag(['<c-t>k', '<c-t>l'])
    def goToNextTab(self): 
        self.m_uiman.goTo(vkind='tab', kind='next')

    @tag(['<c-t>j', '<c-t>h'])
    def goToPrevTab(self): 
        self.m_uiman.goTo(vkind='tab', kind='prev')

    @tag('<c-t>gg')
    def goToFirstTab(self):
        self.m_uiman.goTo(vkind='tab', digit=1)

    @tag(['gt', '<c-t>G'])
    def goToTab(self, digit=None):
        self.m_uiman.goTo(vkind='tab', digit=digit)

    @tag('<c-t>c')
    def addCopyTab(self):
        self.m_uiman.add(vkind='tab', copy=True)

    @tag('<c-t>n')
    def addTab(self):
        self.m_uiman.add(vkind='tab')

    @tag('<c-t>x')
    def closeTab(self):
        self.m_uiman.close(vkind='tab')

    @tag('<c-d>H')
    def hideAllDocks(self): 
        self.m_uiman.docks.hideAll()

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
