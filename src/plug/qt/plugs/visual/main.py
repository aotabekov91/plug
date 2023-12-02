from PyQt5 import QtCore
from plug.qt import Plug
from gizmo.utils import tag

class Visual(Plug):

    isMode=True 
    name='visual' 
    default='select'
    listen_leader='v'

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
            self.setSubmode(self.default)
            self.app.earman.clearKeys()
            self.key=''

    def startHint(self, submode):

        v=self.app.handler.view()
        if self.checkProp('canHint', v):
            v.hintSelected.connect(self.selectHint)
            v.hintFinished.connect(self.finishHint)
            self.setSubmode(submode)
            v.startHint()
            self.key=''

    def finishHint(self):

        v=self.app.handler.view()
        if self.checkProp('canHint', v):
            self.app.earman.clearKeys()
            v.hintFinished.disconnect(self.finishHint)
            self.setSubmode(self.default)
            self.key=''

    def activate(self):

        super().activate()
        self.setSubmode(self.default)

    def octivate(self):

        super().octivate()
        self.setSubmode()

    def go(self, *args, **kwargs):

        v=self.app.handler.view()
        if self.checkProp('hasBlocks', v):
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

    @tag('j', modes=['visual[select]']) 
    def down(self, digit=1):
        self.go(kind='down', digit=digit)

    @tag('k', modes=['visual[select]']) 
    def up(self, digit=1):
        self.go(kind='up', digit=digit)

    @tag('K', modes=['visual[select]']) 
    def screenUp(self, digit=1):
        self.go(kind='screenUp', digit=digit)

    @tag('J', modes=['visual[select]']) 
    def screenDown(self, digit=1):
        self.go(kind='screenDown', digit=digit)
