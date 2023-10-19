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
            name='input',
            special=special,
            listen_leader='<c-I>',
            delisten_on_exec=False,
            **kwargs
            ):

        self.client=None
        super(Input, self).__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader, 
                delisten_on_exec=delisten_on_exec, 
                **kwargs
                )

    def setup(self):

        super().setup()
        self.ui=InputWidget(self.app)
        self.ui.hide()
        self.ui.modeChanged.connect(
                self.app.moder.detailChanged)
        self.ear.carriageReturnPressed.connect(
                self.on_carriagePressed)
        self.ear.escapePressed.connect(
                self.on_escapePressed)

    def listen(self):

        super().listen()
        self.setFocusedWidget()
        self.showWidget()

    def showWidget(
            self, 
            field=True, 
            label=False
            ):

        if label:
            self.ui.label.show()
        self.ui.show()
        if field:
            self.ui.field.show()
        self.ui.field.setFocus()

    def setFocusedWidget(self):

        qapp=QtWidgets.QApplication
        self.client=qapp.focusWidget()

    def yankText(self):

        f=getattr(self.client, 'text', None)
        if not f:
            f=getattr(self.client, 'toPlainText', None)

        if f:
            text=f()
            self.ui.setText(text)

    def hideClearField(self):

        self.ui.hide()
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
                if self.checkSpecialCharacters(e):
                    e.accept()
                    return True
        return False 

    def setText(self, text):
        self.ui.setText(text)

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

        self.deactivate()
        self.escapePressed.emit()

    def on_carriagePressed(self): 

        self.setClientText()
        self.deactivate()
        self.carraigePressed.emit()

    def deactivate(self):
        
        self.client=None
        self.hideClearField()
        super().deactivate()
