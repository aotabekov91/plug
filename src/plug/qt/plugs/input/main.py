from PyQt5 import QtCore

from plug.qt import Plug
from .widget import VimEditor

class Input(Plug):

    special=['carriage']
    detailChanged=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            name='input',
            special=special,
            position='overlay',
            listen_leader='<c-I>',
            delisten_keys=['escape'],
            **kwargs
            ):
        
        self.follow=True
        super(Input, self).__init__(
                name=name,
                special=special,
                position=position,
                delisten_keys=delisten_keys,
                listen_leader=listen_leader, 
                **kwargs
                )
        self.app.uiman.qapp.focusChanged.connect(
                self.on_focusChanged)
        self.ear.carriageReturnPressed.connect(
                self.pasteText)
        self.setFunctors()
        self.setUI()

    def setUI(self):

        self.uiman.position='overlay'
        self.uiman.setUI(VimEditor())
        self.ui.modeChanged.connect(
                self.detailChanged)
        self.app.window.resized.connect(
                self.ui.updatePosition)

    def setFunctors(
            self, 
            getter=None,
            setter=None,
            ):

        self.getter=getter
        self.setter=setter

    def on_focusChanged(self, old, obj):

        if not self.follow: 
            return
        g=getattr(
                obj, 'toPlainText', None)
        s=getattr(
                obj, 'setPlainText', None)
        if not g: 
            g=getattr(
                    obj, 'text', None)
            s=getattr(
                    obj, 'setText', None)
        self.setFunctors(g, s)

    def listen(self):

        self.follow=False
        self.yankText()
        super().listen()

    def delisten(self):

        self.setFunctors()
        self.follow=True
        super().delisten()

    def setText(self, text):
        self.ui.setText(text)

    def setRatio(self, w=None, h=None):
        self.ui.setRatio(w, h)

    def yankText(self):

        if self.getter:
            text=self.getter()
            self.ui.setText(text)

    def pasteText(self):

        text=self.ui.text()
        if self.setter:
            self.setter(text)
        self.deactivate()

    def deactivate(self):
        
        self.setRatio()
        self.ui.clear()
        super().deactivate()
