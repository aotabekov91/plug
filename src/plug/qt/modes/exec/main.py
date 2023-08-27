from PyQt5 import QtCore

from plug.qt import PlugObj
from gizmo.widget import ListWidget, Item

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
        self.event_listener.returnPressed.connect(
                self.on_returnPressed)

    def delisten(self):

        super().delisten()
        self.app.window.bar.bottom.hide()
        self.app.window.bar.edit.clear()

    def listen(self):

        super().listen()
        self.app.window.bar.show()
        self.app.window.bar.bottom.show()
        self.app.window.bar.edit.setFocus()

    def on_returnPressed(self): 

        text=self.app.window.bar.edit.text()
        if text:
            cmd=text.split(' ', 1)
            name=cmd[0]
            item=self.ui.currentItem()
            if item:
                name=item.itemData['up']
                if name in self.commands:
                    method=self.commands[name]
                    method()
        self.delistenWanted.emit()
