from PyQt5 import QtCore, QtWidgets

from plug.qt import Plug
from .widget import InputWidget

class Input(Plug):

    special=[
            'carriage', 
            'escape_bracket'
            ]
    tabPressed=QtCore.pyqtSignal()
    textChanged=QtCore.pyqtSignal()
    textCreated=QtCore.pyqtSignal(object)

    def __init__(
            self, 
            name='input',
            special=special,
            position='overlay',
            listen_leader='<c-I>',
            **kwargs
            ):

        self.setter=None
        self.getter=None
        super(Input, self).__init__(
                name=name,
                special=special,
                position=position,
                listen_leader=listen_leader, 
                **kwargs
                )

    def setup(self):

        super().setup()
        self.qapp=self.app.uiman.qapp
        self.ear.carriageReturnPressed.connect(
                self.on_carriagePressed)
        self.ear.escapePressed.connect(
                self.on_escapePressed)
        self.connect()
        self.setUI()

    def connect(self):

        self.qapp.focusChanged.connect(
                self.on_focusChanged)

    def on_focusChanged(self, old, obj):

        if self.ear.listening:
            return
        getter=getattr(
                obj, 'toPlainText', None)
        setter=getattr(
                obj, 'setPlainText', None)
        if getter:
            self.getter=getter
            self.setter=setter
            return
        getter=getattr(obj, 'text', None)
        setter=getattr(obj, 'setText', None)
        if getter:
            self.getter=getter
            self.setter=setter
            return

    def setUI(self):

        self.uiman.setUI(InputWidget())
        self.ui.modeChanged.connect(
                self.app.moder.detailChanged)

    def listen(self):

        self.yankText()
        super().listen()
        self.focusWidget()

    def delisten(self):

        self.setter=None
        self.getter=None
        super().delisten()

    def focusWidget(
            self, 
            field=True, 
            label=False
            ):

        if label:
            self.ui.label.show()
        if field:
            self.ui.field.show()
        self.ui.field.setFocus()

    def setRatio(self, w=None, h=None):
        self.ui.setRatio(w, h)

    def setText(self, text):
        self.ui.setText(text)

    def yankText(self):

        if self.getter:
            text=self.getter()
            self.ui.setText(text)

    def hideClearField(self):

        self.ui.label.hide()
        self.ui.field.hide()
        self.ui.field.clear()
        self.ui.label.clear()
        self.ui.modeChanged.emit(None)

    def pasteText(self):

        text=self.ui.field.text()
        self.textCreated.emit(text)
        if self.setter:
            self.setter(text)

    def on_escapePressed(self): 

        self.escapePressed.emit()
        self.deactivate()

    def on_carriagePressed(self): 

        self.carriagePressed.emit()
        self.pasteText()
        self.deactivate()

    def deactivate(self):
        
        self.hideClearField()
        super().deactivate()
