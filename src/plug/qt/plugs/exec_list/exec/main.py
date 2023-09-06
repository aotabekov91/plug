from PyQt5 import QtCore

from plug.qt import PlugObj

from .widget import ListWidget

class Exec(PlugObj):

    special=['return', 
            'carriage', 
            'escape', 
            'escape_bracket']

    def __init__(self, 
                 app=None, 
                 name='exec',
                 special=special,
                 listen_leader='<c-e>',
                 **kwargs
                 ):

        super().__init__(
                app=app, 
                name=name, 
                special=special,
                listen_leader=listen_leader, 
                **kwargs
                )
        self.options={}
        self.commands={}
        self.event_listener.returnPressed.connect(
                self.on_returnPressed)
        self.event_listener.tabPressed.connect(
                self.on_tabPressed)
        self.event_listener.keysSet.connect(
                self.on_keysSet)
        self.setUI()

    def setUI(self):

        self.ui=ListWidget(
                self.app,
                objectName='ExecList',
                )
        self.ui.hide()

    def delisten(self):

        super().delisten()
        self.app.window.bar.bottom.hide()
        self.app.window.bar.edit.clear()

    def listen(self):

        super().listen()
        self.app.window.bar.show()
        self.app.window.bar.bottom.show()
        self.app.window.bar.edit.setFocus()

    def addOptions(self, name, option_list):

        self.options[name]=option_list

    def on_keysSet(self, commands):

        self.commands = self.event_listener.methods

    def on_tabPressed(self):

        col=self.getMethods()

        if not self.ui.isVisible():

            if len(col)==1:
                name, method=col[0]
                options=self.options.get(name, None)
                print(options)
                if options:
                    for o in options: 
                        self.ui.list.addItem(o)
                    self.ui.show()

        else:
            pass

    def on_returnPressed(self): 

        col=self.getMethods()
        if len(col)==1: 
            name, method = col[0]
            method()
        self.delistenWanted.emit()

    def getMethods(self):

        name=self.app.window.bar.edit.text()
        method=self.commands.get(name)
        col=[]
        if method:
            col+=[(name, method)]
        else:
            for n, m in self.commands.items():
                if n[len(name)]==name: 
                    col+=[(n, m)]
        return col
