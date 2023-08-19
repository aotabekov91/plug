from PyQt5 import QtCore

from plug.qt.modes.base import Mode
from gizmo.widget import ListWidget, Item

class Exec(Mode):

    escapePressed=QtCore.pyqtSignal()

    def __init__(self, 
                 app=None, 
                 name='exec',
                 listen_leader='Ctrl+e',  
                 delisten_on_exec=False,
                 **kwargs
                 ):

        super().__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader, 
                **kwargs
                )

        self.setUI()

    def checkSpecialCharacters(self, event):

        r=super().checkSpecialCharacters(event)
        accept=['tab',
                'return', 
                'carriage', 
                'escape', 
                'escape_bracket']
        if r in accept:
            return r
        else:
            return False

    def setUI(self):

        self.ui=ListWidget(item_widget=Item)
        self.ui.setParent(self.app.window)

        style_sheet=self.ui.styleSheet()
        style_sheet+='''
            QListWidget{
                border-width: 0px;
                border-color: transparent;
                background-color: transparent;
            }
            QListWidget::item{
                border-width: 0px;
                border-radius: 0px;
            }
            QListWidget::item:selected{
                border-width: 0px;
                background-color: gray;
                border-color: transparent;
            }
        '''

        self.ui.setStyleSheet(style_sheet)
        self.ui.setSpacing(0)

        data=[{'up': n} for n in self.commands.keys()]

        self.ui.setList(data)
        self.ui.hide()

    def saveCommands(self, plug, method, key):
        self.commands[method.name]=method

    def delisten(self):

        super().delisten()
        self.app.window.bar.bottom.hide()
        self.app.window.bar.edit.textChanged.disconnect(
                self.on_textChanged)

        self.app.window.bar.edit.clear()
        self.ui.unfilter()

    def listen(self):

        super().listen()

        self.app.window.bar.show()
        self.app.window.bar.bottom.show()
        self.app.window.bar.edit.setFocus()

        self.app.window.bar.edit.textChanged.connect(
                self.on_textChanged)

        self.ui.show()

    def on_textChanged(self):

        text=self.app.window.bar.edit.text()
        if text: self.ui.filter(text)

    def showList(self, text=None): 

        if text:
            self.ui.filter(text)

            suited=[]
            for name in self.commands.keys():
                if text==name[:len(text)]:
                    suited+=[{'up':name}]
        else:
            suited=self.commands

        if len(suited)==1:
            name=suited[0]['up']
            self.app.window.bar.edit.setText(name)
            self.ui.hide()
        else:
            self.ui.show()

    def on_tabPressed(self): 

        text=self.app.window.bar.edit.text()
        self.showList(text)

    def on_returnPressed(self): 

        text=self.app.window.bar.edit.text()
        if text:
            cmd=text.split(' ', 1)
            name=cmd[0]
            if name in self.commands:
                method=self.commands[name]
                method()

        self.ui.hide()
        self.on_escapePressed()

    def eventFilter(self, w, e):

        if self.listening: 
            if  e.type()==QtCore.QEvent.Enter:
                e.accept()
                return True
            if e.type()==QtCore.QEvent.KeyPress:
                if self.checkSpecialCharacters(e):
                    e.accept()
                    return True
        return False
