from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..base import List, Input
from ..base import UpDownLabel

class InputList (QWidget):

    inputTextChanged=pyqtSignal()
    inputReturnPressed=pyqtSignal()
    listReturnPressed=pyqtSignal()
    contentChanged=pyqtSignal(object)

    def __init__(self, widget_class=UpDownLabel): 
        super(InputList, self).__init__(objectName='mainWidget')

        self.dlist = []
        self.temp_dlist = []
        self.filterShow=True

        self.widget_class=widget_class

        layout, style_sheet=self.setUI()
        self.setLayout(layout)
        self.setStyleSheet(style_sheet)

    def setUI(self):
        style_sheet='''
            QWidget{
                font-size: 16px;
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
        
        self.input=Input(self)
        self.list=List(self)

        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 10)

        layout.addWidget(self.input)
        layout.addWidget(self.list)

        self.input.returnPressed.connect(self.inputReturnPressed)
        self.input.textChanged.connect(self.inputTextChanged)
        self.input.textChanged.connect(self.filterList)

        return layout, style_sheet

    def installEventFilter(self, listener):
        self.input.installEventFilter(listener)
        self.list.installEventFilter(listener)

    def setList(self, dlist, widgetLimit=30):
        if dlist is None: dlist=[]
        self.dlist=dlist
        self.temp_dlist=dlist
        self.addItems(dlist, widgetLimit=widgetLimit)

    def disableFilterShow(self):
        self.filterShow=False

    def enableFilterShow(self):
        self.filterShow=True

    def filterList(self):
        if self.filterShow:
            text=self.input.text()
            self.list.clear()
            dlist=[]
            if len(self.dlist)==0: 
                dlist=[{'up': text}] 
            else:
                if not text:
                    dlist=self.dlist
                else:
                    tmp=self.widget_class()
                    for data in self.dlist:
                        if tmp.isCompatible(text, data):
                            dlist+=[data]
            self.addItems(dlist, False)
            self.temp_dlist=dlist

    def tempList(self):
        return self.temp_dlist

    def sizeHint(self):
        input_hint=self.input.sizeHint()
        list_hint=self.list.sizeHint()
        height=input_hint.height()+list_hint.height()+2 # 2 setSpacing
        return QSize(input_hint.width(), height)

    def addItems(self, dlist, save=True, widgetLimit=100):
        self.list.clear()
        if save: self.dlist = dlist
        if dlist is None or len(dlist)==0: 
            dlist=[{'up': 'No matches are found'}]
        widgets=[]
        for i, d in enumerate(dlist):
            widgets+=[self.addItem(d)]
            if widgetLimit and i>widgetLimit: 
                break

        self.adjustSize()
        self.setItemSizeHints()
        self.list.setCurrentRow(0)

    def setItemSizeHints(self):
        width=self.size().width()
        for i in range(self.list.count()):
            item=self.list.item(i)
            widget=self.list.itemWidget(item)
            widget.setFixedWidth(width-20)
            item.setSizeHint(widget.sizeHint())

    def currentRow(self):
        return self.list.currentRow()

    def currentItem(self):
        return self.list.currentItem()

    def setCurrentItem(self, iid):
        for i in range(self.list.count()):
            item=self.list.item(i)
            if item.itemData['id']==iid:
                self.list.setCurrentItem(item)
                return

    def setCurrentRow(self, row):
        if row<0:
            row=0
        elif row-1>self.list.count():
            row=self.index.count()-1
        self.list.setCurrentRow(row)

    def addItem(self, w):
        item = QListWidgetItem(self.list)
        item.itemData = w
        widget = self.widget_class()
        widget.setData(w)
        self.list.addItem(item)
        self.list.setItemWidget(item, widget)
        if hasattr(widget, 'contentChanged'):
            widget.contentChanged.connect(self.contentChanged)
        return widget

    def move(self, crement=-1):
        crow = self.list.currentRow()
        if crow==None: return
        crow += crement
        if crow < 0:
            crow = self.list.count()-1
        elif crow >= self.list.count():
            crow = 0
        self.list.setCurrentRow(crow)

    def setFocus(self):
        if self.input.isVisible():
            self.input.setFocus()
        else:
            self.list.setFocus()

    def focusList(self):
        self.list.setFocus()

    def focusInput(self):
        self.input.setFocus()

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Down, Qt.Key_Up]:
            self.list.keyPressEvent(event)
        elif event.key()==Qt.Key_I:
            if self.input.isVisible():
                self.input.hide()
                self.list.setFocus()
            else:
                self.input.show()
                self.input.setFocus()
        elif event.modifiers() or self.list.hasFocus():
            if event.key() in [Qt.Key_J, Qt.Key_N]:
                self.move(crement=1)
            elif event.key() in [Qt.Key_K, Qt.Key_P]:
                self.move(crement=-1)
            elif event.key() in  [Qt.Key_L, Qt.Key_M, Qt.Key_Enter]:
                self.listReturnPressed.emit()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def setInputText(self, text):
        self.input.setText(text)
    
    def inputText(self):
        return self.input.text()

    def clearInput(self):
        self.input.clear()

    def clear(self):
        self.dlist=[]
        self.input.clear()
        self.list.clear()

    def hideInput(self):
        self.input.hide()

    def showInput(self):
        self.input.show()

    def resizeEvent(self, event):
        self.input.setFixedWidth(self.size().width())
        self.setItemSizeHints()
