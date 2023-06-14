from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..list import InputList
from ..base import Stack, UpLabel

class InputListLabelStack (Stack):

    inputTextChanged=pyqtSignal()
    inputReturnPressed=pyqtSignal()
    listReturnPressed=pyqtSignal()
    contentChanged=pyqtSignal(object)

    def __init__(self): 
        super(InputListLabelStack, self).__init__()

        self.setUI()

    def setUI(self):

        self.main=InputList(widget_class=UpLabel)
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
