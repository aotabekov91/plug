from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .mode import Modes
from .buffer import Buffer
from .plugin import Plugins

class Manager(QObject):

    bufferCreated=pyqtSignal(object)

    def __init__(self, app, buffer_class=Buffer):

        super(Manager, self).__init__(app)

        self.app=app
        self.actions={}

        self.app.modes=Modes(app)
        self.app.plugins=Plugins(app)

        self.setBuffer(buffer_class)

    def register(self, plugin, actions): 

        self.actions[plugin]=actions
        self.app.actionRegistered.emit()

    def setBuffer(self, buffer_class): 

        self.app.buffer=buffer_class(self.app)
        self.app.buffer.bufferCreated.connect(self.bufferCreated)
