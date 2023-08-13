from PyQt5 import QtCore, QtWidgets

from ..base import Mode
from .widget import InputWidget

class Input(Mode):

    escapePressed=QtCore.pyqtSignal()

    def __init__(self, 
                 app=None, 
                 name='input',
                 listen_leader='Ctrl+;',  
                 delisten_on_exec=False,
                 **kwargs
                 ):

        super().__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader, 
                delisten_on_exec=delisten_on_exec, 
                **kwargs
                )

        self.client=None
        self.widget=InputWidget(self.app)
        self.widget.hide()

    def listen(self):

        super().listen()
        self.client=QtWidgets.QApplication.focusWidget()
        self.yankText()
        self.showField()

    def yankText(self):

        f=getattr(self.client, 'text', None)
        if not f:
            f=getattr(self.client, 'toPlainText', None)

        if f:
            text=f()
            self.widget.setText(text)

    def showField(self, field=True, label=False):

        self.widget.show()
        if field:
            self.widget.field.show()
        if label:
            self.widget.label.show()

        self.widget.field.setFocus()

    def hideClearField(self):

        self.widget.hide()
        self.widget.label.hide()
        self.widget.field.hide()

        self.widget.field.clear()
        self.widget.label.clear()

    def eventFilter(self, w, e):

        if self.listening:
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

            f=getattr(self.client, 'setText', None)
            if not f:
                f=getattr(self.client, 'setPlainText', None)

            if f: 
                text=self.widget.field.text()
                if text: f(text)

    def checkSpecialCharacters(self, event):

        r=super().checkSpecialCharacters(event)
        if r in ['escape_bracket', 'carriage']:
            return True
        else:
            return False

    def on_escapePressed(self): 

        super().on_escapePressed()
        self.forceDelisten.emit()
        self.client=None
        if self.widget.isVisible(): self.hideClearField()

    def on_carriagePressed(self): 

        self.setText()
        self.returnPressed.emit()
        self.forceDelisten.emit()
        self.client=None
        if self.widget.isVisible(): self.hideClearField()
