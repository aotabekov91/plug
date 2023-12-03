from PyQt5 import QtCore
from plug.qt import Plug
from gizmo.utils import tag

class Visual(Plug):

    isMode=True 
    name='visual' 
    listen_leader='v'

    def activate(self):

        self.setSubmode()
        super().activate()

    def event_functor(self, e, ear):

        t=e.text()
        sm=self.submode()
        v=self.app.handler.view()
        if sm in ['hint', 'jump'] and t: 
            self.key+=t
            v.updateHint(self.key)
            return True

    def selectHint(self, sel):

        v=self.app.handler.view()
        if self.checkProp('canHint', v):
            v.selectHint(sel, self.submode()) 
            self.app.earman.clearKeys()
            self.key=''

    def startHint(self, submode):

        v=self.app.handler.view()
        if self.checkProp('canHint', v):
            self.setSubmode('hint')
            v.hintSelected.connect(self.selectHint)
            v.hintFinished.connect(self.finishHint)
            f=getattr(v, 'startHint', None)
            if f: f(submode)
            self.key=''

    def finishHint(self):

        v=self.app.handler.view()
        if self.checkProp('canHint', v):
            self.setSubmode()
            self.app.earman.clearKeys()
            v.hintFinished.disconnect(self.finishHint)
            f=getattr(v, 'finishHint', None)
            if f: f()
            self.key=''

    def go(self, *args, **kwargs):

        v=self.app.handler.view()
        if self.checkProp('hasVisual', v):
            v.go(*args, mode='visual', **kwargs)

    @tag('<c-j>', modes=['visual']) 
    def setJumpSubmode(self):
        self.startHint('jump')

    @tag('<c-h>', modes=['visual']) 
    def setHintSubmode(self):
        self.startHint('hint')

    @tag('<c-s>', modes=['visual']) 
    def setSelectSubmode(self):
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
