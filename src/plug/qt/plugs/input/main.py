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
            app=None, 
            special=special,
            position='overlay',
            listen_leader='<c-I>',
            delisten_on_exec=False,
            **kwargs
            ):

        self.client=None
        super(Input, self).__init__(
                app=app, 
                position=position,
                listen_leader=listen_leader, 
                delisten_on_exec=delisten_on_exec, 
                **kwargs
                )

    def setup(self):

        super().setup()
        self.ear.carriageReturnPressed.connect(
                self.on_carriagePressed)
        self.ear.escapePressed.connect(
                self.on_escapePressed)
        self.setUI()

    def setUI(self):

        self.uiman.setUI(InputWidget())
        self.ui.modeChanged.connect(
                self.app.moder.detailChanged)

    def listen(self):

        super().listen()
        self.showWidget()
        self.setFocusedWidget()

    def showWidget(
            self, 
            field=True, 
            label=False
            ):

        if label:
            self.ui.label.show()
        if field:
            self.ui.field.show()
        self.ui.field.setFocus()

    def setFocusedWidget(self):

        qapp=QtWidgets.QApplication
        self.client=qapp.focusWidget()

    def yankText(self):

        g=getattr(
                self.client, 
                'toPlainText',
                None
                )
        f=getattr(
                self.client, 
                'text',
                g
                )
        if f:
            self.ui.setText(f())

    def hideClearField(self):

        self.ui.label.hide()
        self.ui.field.hide()
        self.ui.field.clear()
        self.ui.label.clear()
        self.ui.modeChanged.emit(None)

    def eventFilter(self, w, e):

        if self.ear.listening:
            if  e.type()==QtCore.QEvent.Enter:
                e.accept()
                return True
            elif  e.type()==QtCore.QEvent.KeyPress:
                if self.checkSpecial(e):
                    e.accept()
                    return True
        return False 

    def setText(self, text):
        self.ui.setText(text)

    def setRatio(self, w=None, h=None):
        self.ui.setRatio(w, h)

    def setClientText(self):

        text=self.ui.field.text()
        self.textCreated.emit(text)
        if self.client:
            gunc=getattr(
                    self.client, 
                    'setPlainText', 
                    None)
            func=getattr(
                    self.client, 
                    'setText', 
                    gunc)
            if func and text: 
                func(text)

    def on_escapePressed(self): 

        self.escapePressed.emit()
        self.deactivate()

    def on_carriagePressed(self): 

        self.carriagePressed.emit()
        self.setClientText()
        self.deactivate()

    def deactivate(self):
        
        self.client=None
        self.hideClearField()
        super().deactivate()
