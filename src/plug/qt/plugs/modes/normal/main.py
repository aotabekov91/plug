from PyQt5 import QtGui, QtCore

from plug.qt import Plug
from gizmo.utils import register

class Normal(Plug):

    def __init__(self, 
                 app=None,
                 name='normal',
                 listen_leader='@',
                 delisten_on_exec=False,
                 **kwargs,
                 ):

        self.cursor_visible=True

        super(Normal, self).__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader,
                delisten_on_exec=delisten_on_exec, 
                **kwargs,)

        self.display=self.app.display
        self.app.installEventFilter(self)

    def currentView(self):
        return self.display.currentView()

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

    @register(key='G')
    def gotoEnd(self):

        view=self.currentView()
        if view: 
            view.gotoEnd()

    @register(key='gg')
    def gotoBegin(self):

        view=self.currentView()
        if view: 
            view.gotoBegin()

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

    @register(key='g')
    def goto(self, digit=1):

        view=self.currentView()
        if view: 
            view.goto(digit)

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

    @register(key='tc', modes=['normal', 'command'])
    def toggleCursor(self): 

        if self.cursor_visible:
            c=QtGui.QCursor(QtCore.Qt.BlankCursor)
        else:
            c=QtGui.QCursor(QtCore.Qt.ArrowCursor)
        self.cursor_visible=not self.cursor_visible
        self.app.setOverrideCursor(c)

    @register(key='<c-w>sv', modes=['normal', 'command'])
    def splitVertical(self): 

        if self.currentView():
            self.display.split(False)

    @register(key='<c-w>sh', modes=['normal', 'command'])
    def splitHorizontal(self):

        if self.currentView():
            self.display.split(True)

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

    def eventFilter(self, widget, event):

        if event.type()==QtCore.QEvent.MouseMove:
            if not self.cursor_visible:
                event.accept()
                return True
        return False
