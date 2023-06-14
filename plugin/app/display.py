from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .plugin import Configure

class Display(QSplitter):

    viewCreated=pyqtSignal(object)
    viewChanged=pyqtSignal(object)
    currentItemChanged=pyqtSignal(object)

    hoverMoveOccured=pyqtSignal(object, object)
    mouseMoveOccured=pyqtSignal(object, object)
    mousePressOccured=pyqtSignal(object, object)
    mouseReleaseOccured=pyqtSignal(object, object)
    mouseDoubleClickOccured=pyqtSignal(object, object)

    def __init__(self, app, window, view_class=None):

        super().__init__(parent=window)

        self.app=app
        self.win=window
        self.view_class=view_class

        self.count=-1
        self.views={}
        self.view=None

        self.configure=Configure(app, 'Display', self, mode_keys={'command': 'w'})

        self.setUI()

    def setViewClass(self, view_class): self.view_class=view_class

    def setUI(self):

        self.m_hlayout=QVBoxLayout(self)#.m_hsplit)
        self.m_hlayout.setSpacing(0)
        self.m_hlayout.setContentsMargins(0,0,0,0)

        self.setContextMenuPolicy(Qt.NoContextMenu)

    def clear(self):

        for index in range(self.m_hlayout.count(),-1, -1):
            item=self.m_hlayout.takeAt(index)
            if item: item.widget().hide()
        self.hide()

    def setView(self, view, how=None, focus=True):

        self.setCurrentView(view)

        if how=='reset':
            self.clear()
            self.m_hlayout.addWidget(view)
            self.show()
        elif how=='below':
            self.m_hlayout.addWidget(view)
            self.show()

        view.show()

        if focus: view.setFocus()

    def addView(self, view):

        self.m_hlayout.addWidget(view)

    def focus(self, increment=1):

        if self.m_hlayout.count()<2:
            view=self.currentView()
            if view: view.setFocus()
        else:
            currentView=self.currentView()
            index=self.indexOf(currentView)
            index+=increment
            if index>=self.m_hlayout.count():
                index=0
            elif index<0:
                index=self.m_hlayout.count()-1
            view=self.widget(index)
            self.setCurrentView(view)
        self.focusCurrentView()

    def closeView(self, view=None, vid=None):

        if view is None:
            view=self.currentView()
        if vid is None and view:
            vid=view.id()
        index=None
        for f in range(self.m_hlayout.count()):
            item=self.m_hlayout.itemAt(f)
            if item and item.widget().id()==vid:
                view=item.widget()
                index=f
                break
        if not index is None:
            self.m_hlayout.removeWidget(view)
            view.close()
            index-=1
            if index<0: index=0
            if self.m_hlayout.count()>0:
                view=self.widget(index)
                self.setCurrentView(view)
                self.focusCurrentView()

    def open(self, model=None, how='reset', focus=True):

        if how=='rest':
            if self.view and self.view.model()==model: return

        view=self.createView(model)
        if view: self.setView(view, how, focus)

    def createView(self, model):

        if self.view_class:

            self.count+=1
            view=self.view_class(self.app)
            view.setModel(model)
            self.views[self.count]=view
            self.viewCreated.emit(view)

            return view

    def currentView(self): return self.view

    def setCurrentView(self, view):

        if view!=self.view: 
            self.view=view
            self.viewChanged.emit(self.view)

    def incrementUp(self, digit=1): 

        for d in range(digit): self.view.incrementUp()

    def incrementDown(self, digit=1): 

        for d in range(digit): self.view.incrementDown()

    def incrementLeft(self, digit=1): 

        for d in range(digit): self.view.incrementLeft()

    def incrementRight(self, digit=1): 

        for d in range(digit): self.view.incrementRight()

    def zoomIn(self, digit=1): 
        
        for d in range(digit): self.view.changeScale(kind='zoomIn')

    def zoomOut(self, digit=1): 
        
        for d in range(digit): self.view.changeScale(kind='zoomOut')

    def adjust(self): self.view.readjust()
