from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..base import StackWidget
from .input_list import InputList
from .command_list import CommandList
from ..base import UpDownLabel, ListWidget, InputLabelWidget

class InputListStack(StackWidget):

    returnPressed=pyqtSignal()
    listReturnPressed=pyqtSignal()
    inputReturnPressed=pyqtSignal()
    inputTextChanged=pyqtSignal()

    def __init__(self, list_class=ListWidget, 
                 input_class=InputLabelWidget, 
                 item_class=UpDownLabel,
                 input_list=InputList): 
        super(InputListStack, self).__init__()

        self.setUI(item_class, list_class, input_class, input_list)
        self.addWidget(CommandList(), 'commands')

    def setUI(self, item_class, list_class, input_class, input_list):
        self.main=input_list(item_class, list_class, input_class)
        self.main.returnPressed.connect(self.returnPressed)
        self.main.inputTextChanged.connect(self.inputTextChanged)
        self.main.listReturnPressed.connect(self.listReturnPressed)
        self.main.inputReturnPressed.connect(self.inputReturnPressed)
        self.main.hideWanted.connect(self.hide)
        self.setMainWidget(self.main)

    def setInputWidget(self, inputWidget):
        self.main.setInputWidget(inputWidget)

    def setListWidget(self, listWidget):
        self.main.setListWidget(listWidget)

    def toggleCommands(self):
        if self.currentWidget()==self.commands:
            self.showMainWidget()
        else:
            self.setCurrentWidget(self.commands)

    def installEventFilter(self, listener):
        super().installEventFilter(listener)
        self.commands.setSource(listener)

    def show(self):
        if self.parent() and not self.parent().isVisible():
            self.parent().show()
        self.showCurrentWidget()

    def hide(self):
        if self.parent() and self.parent().isVisible():
            self.parent().hide()
