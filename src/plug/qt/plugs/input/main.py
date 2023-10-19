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
                self.on_returnPressed)
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

    def setText(self):

        if self.client:
            f=getattr(
                    self.client, 
                    'setText', 
                    None
                    )
            if not f:
                f=getattr(
                        self.client, 
                        'setPlainText', 
                        None
                        )

            if f: 
                text=self.ui.field.text()
                if text: f(text)

    def on_escapePressed(self): 

        self.client=None
        self.deactivate()
        self.hideClearField()
        self.escapePressed.emit()

    def on_returnPressed(self): 

        self.setText()
        self.client=None
        self.deactivate()
        self.hideClearField()
        self.returnPressed.emit()
