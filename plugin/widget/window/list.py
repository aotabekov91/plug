from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..list import ListWidget 
from .central import CentralWindow

class ListWindow (CentralWindow):

    returnPressed=pyqtSignal()
    inputTextChanged=pyqtSignal()
    inputReturnPressed=pyqtSignal()
    listReturnPressed=pyqtSignal()

    def __init__(self, app, window_title='', label_title=''):
        super(ListWindow, self).__init__(app, window_title)

        self.setGeometry(0, 0, 700, 500)

        self.list=ListWidget(label_title)

        self.list.inputReturnPressed.connect(self.inputReturnPressed)
        self.list.listReturnPressed.connect(self.listReturnPressed)
        self.list.inputReturnPressed.connect(self.returnPressed)
        self.list.listReturnPressed.connect(self.returnPressed)
        self.list.inputTextChanged.connect(self.inputTextChanged)


        self.setMainWidget(self.list)
        self.setCurrentWidget(self.list)

    def setList(self, dlist, widgetLimit=30):
        self.currentWidget().setList(dlist, widgetLimit)

    def disableFilterShow(self):
        self.currentWidget().disableFilterShow()

    def enableFilterShow(self):
        self.currentWidget().enableFilterShow()

    def doneAction(self, *args, **kwargs):
        self.currentWidget().clear()
        self.hide()

    def setInputText(self, text):
        self.currentWidget().setInput.Text(text)
    
    def inputText(self):
        return self.currentWidget().inputText()

    def setLabelText(self, text):
        self.currentWidget().setLabelText(text)

    def labelText(self):
        return self.currentWidget().labelText()

    def clear(self):
        self.currentWidget().clear()

    def currentItem(self):
        return self.currentWidget().currentItem()

    def setCurrentRow(self, row):
        # if hasattr(self.currentWidget(), 'setCurrentRow'):
        self.currentWidget().setCurrentRow(row)

    def currentRow(self):
        return self.currentWidget().currentRow()
