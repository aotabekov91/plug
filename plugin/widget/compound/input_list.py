from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..base import IconUpDown, ListWidget, InputLabelWidget

class InputList (QWidget):

    hideWanted=pyqtSignal()
    returnPressed=pyqtSignal()

    inputTextChanged=pyqtSignal()
    inputReturnPressed=pyqtSignal()
    listReturnPressed=pyqtSignal()

    def __init__(self, 
                 list_class=ListWidget,
                 input_class=InputLabelWidget, 
                 **kwargs): 

        super(InputList, self).__init__(objectName='mainWidget')

        self.setInputWidget(input_class)
        self.setListWidget(list_class, **kwargs)

        self.input_focused=True

        self.setUI()

        self.setMinimumSize(400, 600)

    def setListWidget(self, list_class, **kwargs):

        if list_class:

            self.list=list_class(**kwargs)
            self.list.hideWanted.connect(self.hideWanted)
            self.list.openWanted.connect(self.list.focusItem)
            self.list.returnPressed.connect(self.returnPressed)
            self.list.returnPressed.connect(self.listReturnPressed)

    def setInputWidget(self, input_class):

        if input_class:
            self.input=input_class()
            self.input.hideWanted.connect(self.hideWanted)
            self.input.returnPressed.connect(self.returnPressed)
            self.input.returnPressed.connect(self.inputReturnPressed)
            self.input.textChanged.connect(self.filter)
            self.input.textChanged.connect(self.inputTextChanged)

    def setUI(self):

        style_sheet='''
            QWidget{
                font-size: 15px;
                color: white;
                border-width: 0px;
                background-color: #101010; 
                border-color: transparent;
                }
            QWidget#mainWidget{
                border-radius: 10px;
                border-style: outset;
                background-color: transparent; 
                }
                '''
        
        layout = QVBoxLayout()

        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.input)
        layout.addWidget(self.list)

        self.setLayout(layout)
        self.setStyleSheet(style_sheet)

    def installEventFilter(self, listener):

        self.input.installEventFilter(listener)
        self.list.installEventFilter(listener)

    def setList(self, dlist, limit=30): 

        self.list.setList(dlist, limit)
        self.adjustSize()

    def setEnableFilter(self, condition): self.list.setEnableFilter(condition)

    def filter(self): self.list.filter(self.input.text())

    def dataList(self): return self.list.dlist

    def filterList(self): return self.list.flist

    def setFocus(self):

        if self.input.isVisible():
            self.input.setFocus()
        else:
            self.list.setFocus()

    def keyPressEvent(self, event):

        if event.modifiers()==Qt.ControlModifier:  
            if event.key() in [Qt.Key_J, Qt.Key_N]:
                self.list.move(crement=1)
            elif event.key() in [Qt.Key_K, Qt.Key_P]:
                # TODO :bug: Key_K does not work
                self.list.move(crement=-1)
            elif event.key() == Qt.Key_L:
                self.focusItem()
            elif event.key() in [Qt.Key_I]:
                self.toggleFocus()
        else:
            super().keyPressEvent(event)

    def toggleFocus(self):

        if self.input_focused:
            self.input_focused=False
            self.list.setFocus()
        else:
            self.input_focused=True
            self.input.setFocus()

    def focusItem(self):

        item=self.list.currentItem()
        if item: self.list.itemWidget(item).setFocus()

    def clear(self): self.input.clear()

    def toggleInput(self):

        if self.input.isVisible():
            self.input.hide()
            self.list.setFocus()
        else:
            self.input.show()
            self.input.setFocus()

    def resizeEvent(self, event): 

        super().resizeEvent(event)
        self.adjustSize()

    def adjustSize(self):

        width=self.size().width()
        height=self.size().height()

        if self.parent(): 
            width=self.parent().size().width()
            height=self.parent().size().height()

        height=height-self.input.size().height()-5

        self.input.setFixedWidth(width)
        self.list.adjustSize(width, height)

        super().adjustSize()
