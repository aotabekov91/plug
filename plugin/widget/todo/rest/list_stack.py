from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..base import Stack
from ..list import InputList
from ..base import UpDownEdit, UpLabel, IconUpDown, UpDownLabel

class BaseList(Stack):

    def __init__(self, item_widget): 
        super(BaseList, self).__init__()

        self.setUI(item_widget)

    def setUI(self, item_widget):
        self.main=InputList(item_widget)
        self.setMainWidget(self.main)

        self.main.inputTextChanged.connect(self.inputTextChanged)
        self.main.listReturnPressed.connect(self.listReturnPressed)
        self.main.inputReturnPressed.connect(self.inputReturnPressed)
        self.main.contentChanged.connect(self.contentChanged)

    def setList(self, dlist):
        self.main.setList(dlist)

    def focusList(self):
        self.setCurrentWidget(self.main)
        self.main.focusList()

    def focusInput(self):
        self.setCurrentWidget(self.main)
        self.main.focusInput()

    def currentItem(self):
        return self.main.currentItem()

    def currentRow(self):
        return self.main.currentRow()

    def setCurrentRow(self, row):
        self.main.setCurrentRow(row)

    def hideInput(self):
        self.main.hideInput()

    def showInput(self):
        self.main.showInput()

class InputListUp(BaseList):
    def __init__(self):
        super().__init__(item_widget=UpLabel)

class InputListEdit(BaseList):
    def __init__(self):
        super().__init__(item_widget=UpDownEdit)

class InputListIcon(BaseList):
    def __init__(self):
        super().__init__(item_widget=IconUpDown)

class InputListUpDown(BaseList):
    def __init__(self):
        super().__init__(item_widget=UpDownLabel)
