from PyQt5 import QtCore
from plug.qt import Plug
from gizmo.utils import tag

class Visual(Plug):

    isMode=True 
    eatEvent=False
    name='visual' 
    listen_leader='v'
    eventFunctor=QtCore.pyqtSignal(object)

    def event_functor(self, e, ear):

        self.eventFunctor.emit(e)
        if self.eatEvent:
            return True

    def go(self, *args, **kwargs):

        v=self.app.handler.view()
        if self.checkProp('hasVisual', v):
            v.go(*args, mode='visual', **kwargs)

    def activate(self):

        super().activate()
        self.setSubmode('select')
        v=self.app.handler.view()
        if v and hasattr(v, 'startVisualMode'):
            v.startVisualMode(self)

    def octivate(self):

        v=self.app.handler.view()
        if v and hasattr(v, 'finishVisualMode'):
            v.finishVisualMode(self)
        super().octivate()

    @tag('<c-s>', modes=['visual'])
    def toggleSelectSubmode(self):

        if self.submode()=='select':
            self.setSubmode()
        else:
            self.setSubmode('select')

    @tag('k', modes=['visual[select]']) 
    def up(self, digit=1):
        self.go(kind='up', digit=digit)

    @tag('j', modes=['visual[select]']) 
    def down(self, digit=1):
        self.go(kind='down', digit=digit)

    @tag('l', modes=['visual[select]']) 
    def left(self, digit=1):
        self.go(kind='left', digit=digit)

    @tag('h', modes=['visual[select]']) 
    def right(self, digit=1):
        self.go(kind='right', digit=digit)

    @tag('K', modes=['visual[select]']) 
    def screenUp(self, digit=1):
        self.go(kind='screenUp', digit=digit)

    @tag('J', modes=['visual[select]']) 
    def screenDown(self, digit=1):
        self.go(kind='screenDown', digit=digit)

    @tag('L', modes=['visual[select]']) 
    def screenRight(self, digit=1):
        self.go(kind='screenRight', digit=digit)

    @tag('H', modes=['visual[select]']) 
    def screenLeft(self, digit=1):
        self.go(kind='screenLeft', digit=digit)
