from PyQt5 import QtCore
from plug.qt import Plug
from gizmo.utils import tag

class Visual(Plug):

    isMode=True 
    name='visual' 
    listen_leader='v'
    hintSelected=QtCore.pyqtSignal(object)
    hintFinished=QtCore.pyqtSignal(object)

    def setup(self):

        self.key=''
        super().setup()

    def event_functor(self, e, ear):

        t=e.text()
        sm=self.submode()
        v=self.app.handler.view()
        if sm in ['hint', 'jump'] and t: 
            self.key+=t
            v.updateHint(self.key)
            return True

    def starthinting(self):

        v=self.app.handler.view()
        v.hintSelected.connect(self.hintSelected)
        v.hintFinished.connect(self.finishHinting)

    def finishHinting(self):

        self.setSubmode('select')
        v=self.app.handler.view()
        self.hintFinished.emit(v)
        self.app.earman.clearKeys()
        v.hintSelected.disconnect(self.hintSelected)
        v.hintFinished.disconnect(self.finishHinting)

    def activate(self):

        super().activate()
        self.setSubmode('select')

    def octivate(self):

        super().octivate()
        self.setSubmode()

    def go(self, *args, **kwargs):

        v=self.app.handler.view()
        if self.checkProp('hasBlocks', v):
            v.go(*args, mode='visual', **kwargs)

            # for i in range(digit):
            #     s=self.view.selection()
            #     if not s: return
            #     i=s['item']
            #     e=i.element()
            #     e.updateBlock(kind, s)
            #     i.update()

    @tag('<c-j>', modes=['visual']) 
    def setJumpSubmode(self):
        self.setSubmode('jump')

    @tag('<c-h>', modes=['visual']) 
    def setHintSubmode(self):

        self.starthinting()
        self.setSubmode('hint')

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
