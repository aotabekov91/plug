from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..input import InputWidget
from .qlistwidget import CustomListWidget, CustomListItem

class ListWidget (QWidget):

    inputTextChanged=pyqtSignal()
    inputReturnPressed=pyqtSignal()
    listReturnPressed=pyqtSignal()

    def __init__(self, label_title=''):
        super(ListWidget, self).__init__(objectName='mainWidget')

        self.style_sheet='''
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
        
        self.dlist = []
        self.filterShow=True

        self.setGeometry(0, 0, 700, 500)

        self.input=InputWidget(self, objectName='inputContainerInput') 
        self.input.setLabel(label_title)
        self.list=CustomListWidget(self)

        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.input)
        layout.addWidget(self.list)

        self.setLayout(layout)
        self.setStyleSheet(self.style_sheet)

        self.input.returnPressed.connect(self.inputReturnPressed)
        self.input.textChanged.connect(self.inputTextChanged)
        self.input.textChanged.connect(self.on_inputTextChanged)

    def installEventFilter(self, listener):
        self.input.installEventFilter(listener)
        self.list.installEventFilter(listener)

    def setList(self, dlist, widgetLimit=30):
        self.dlist=dlist
        self.addItems(dlist, widgetLimit=widgetLimit)

    def disableFilterShow(self):
        self.filterShow=False

    def enableFilterShow(self):
        self.filterShow=True

    def on_inputTextChanged(self):
        if not self.filterShow: return
        text=self.input.text()
        self.list.clear()
        if len(self.dlist)==0: 
            dlist=[{'top': text}] 
        else:
            if not text:
                dlist=self.dlist
            else:
                dlist = []
                for i, w in enumerate(self.dlist):
                    text_up = w.get('top', '')
                    text_down = w.get('down', '')
                    if text:
                        cond1 = text_up and text.lower() in str(text_up).lower() 
                        cond2 = text_down and text.lower() in str(text_down).lower()
                        if cond1 or cond2:
                            dlist += [w]
        self.addItems(dlist, False)

    def sizeHint(self):
        hint=self.input.sizeHint()
        if self.list.count()>0:
            list_hint=self.list.sizeHint()
            hint=QSize(700, hint.height()+list_hint.height())
        return hint

    def addItems(self, dlist, save=True, widgetLimit=100):
        self.list.clear()
        if save: self.dlist = dlist
        if len(dlist)==0: dlist=[{'top': 'No matches are found'}]
        widgets=[]
        for i, d in enumerate(dlist):
            widgets+=[self.addItem(d)]
            if widgetLimit and i>widgetLimit: 
                break

        width=self.size().width()
        height=0
        for i, w in enumerate(widgets):
            if w.size().height()>height:
                height=w.size().height()
        if height<80:
            height=80
        hint=QSize(width, height)
        for i in range(len(widgets)):
            item=self.list.item(i)
            item.setSizeHint(hint)

        self.list.setCurrentRow(0)
        self.adjustSize()

    def addItem(self, w):
        item = QListWidgetItem(self.list)
        widget = CustomListItem()
        item.itemData = w

        widget.setTextUp(w['top'])

        if w.get('down'):
            widget.setTextDown(w.get('down'))

        if w.get('icon', False):
            widget.setIcon(w['icon'])
            widget.iconQLabel.show()

        widget.adjustSize()

        self.list.addItem(item)
        self.list.setItemWidget(item, widget)
        # item.setSizeHint(widget.sizeHint())
        return widget

    def doneAction(self, *args, **kwargs):
        self.list.clear()
        self.input.clear()
        self.hide()

    def move(self, crement=-1):
        crow = self.list.currentRow()
        if crow==None: return
        crow += crement
        if crow < 0:
            crow = self.list.count()-1
        elif crow >= self.list.count():
            crow = 0
        self.list.setCurrentRow(crow)

    def showAction(self, *args, **kwargs): 
        self.hide()
        self.list.show()
        self.show()
        self.input.setFocus()
        
    def hideAction(self, *args, **kwargs): 
        self.hide()

    def setFocus(self):
        self.input.setFocus()

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Down, Qt.Key_Up]:
            self.list.keyPressEvent(event)
        elif event.key()==Qt.Key_I:
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

    def setLabelText(self, text):
        self.input.setLabel(text)

    def labelText(self):
        self.input.label()

    def clear(self):
        self.input.clear()
        self.list.clear()
        self.dlist=[]

    def currentItem(self):
        return self.list.currentItem()
