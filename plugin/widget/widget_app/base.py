from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..base import ListWidget
from ..stack import InputListStack, CommandStack

class BaseAppWidget:

    def __init__(self, plugin, location, *args, **kwargs):

        super(BaseAppWidget, self).__init__(*args, **kwargs)

        self.plugin=plugin
        self.app=plugin.app
        self.activated=False

        self.app.main.docks.setTab(self, location)

    def deactivate(self): 

        if self.activated:

            self.activated=False
            self.plugin.actOnDefocus()
            self.dock.deactivate(self)

    def activate(self): 

        self.activated=True
        self.plugin.actOnFocus()
        self.dock.activate(self)

class BaseListWidget(BaseAppWidget, ListWidget): pass

class BaseCommandStack(BaseAppWidget, CommandStack): pass

class BaseInputListStack(BaseAppWidget, InputListStack): pass
