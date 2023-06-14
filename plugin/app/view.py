from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .plugin import Configure

class View(QGraphicsView):

    keyPressOccured=pyqtSignal(object, object)
    hoverMoveOccured = pyqtSignal(object, object)

    resizeOccured=pyqtSignal(object, object)
    mouseMoveOccured = pyqtSignal(object, object)
    mousePressOccured = pyqtSignal(object, object)
    mouseDoubleClickOccured = pyqtSignal(object, object)
    mouseReleaseOccured = pyqtSignal(object, object)

    def __init__(self, app, layout, scene_class=QGraphicsScene):

        super().__init__(app.main)

        self.app=app

        self.m_model=None
        self.m_selected=[]
        self.configure=Configure(app, 'View', self)

        self.setAcceptDrops(False)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setup(scene_class, layout)

        self.connect()

    def setup(self, scene_class, layout):

        self.setScene(scene_class())
        self.scene().setBackgroundBrush(QColor('black'))
        self.m_layout = layout(self)

    def selected(self): return self.m_selected

    def deselect(self): self.m_selected=[]

    def select(self, selections=[]): 

        if self.m_selected: self.deselect(self.m_selected)
        self.m_selected=selections

    def show(self):

        super().show()
        self.readjust()
        self.setFocus()

    def connect(self):

        self.mouseDoubleClickOccured.connect(self.app.main.display.mouseDoubleClickOccured)
        self.mouseReleaseOccured.connect(self.app.main.display.mouseReleaseOccured)
        self.mouseMoveOccured.connect(self.app.main.display.mouseMoveOccured)
        self.mousePressOccured.connect(self.app.main.display.mousePressOccured)
        self.hoverMoveOccured.connect(self.app.main.display.hoverMoveOccured)

    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.resizeOccured.emit(self, event)
        self.readjust()

    def mouseMoveEvent(self, event):
        
        super().mouseMoveEvent(event)
        self.mouseMoveOccured.emit(self, event)

    def mousePressEvent(self, event):

        super().mousePressEvent(event)
        self.mousePressOccured.emit(self, event)

    def mouseReleaseEvent(self, event):
        
        super().mouseReleaseEvent(event)
        self.mouseReleaseOccured.emit(self, event)

    def mouseDoubleClickEvent(self, event):

        super().mouseDoubleClickEvent(event)
        self.mouseDoubleClickOccured.emit(self, event)

    def readjust(self): pass

    def incrementLeft(self): pass

    def incrementRight(self): pass

    def incrementDown(self): pass

    def incrementUp(self): pass

    def pageUp(self): pass

    def pageDown(self): pass

    def pageLeft(self): pass

    def pageRight(self): pass

    def model(self): return self.m_model

    def setModel(self, model):

        self.scene().clear()
        self.m_model=model

    def zoom(self, kind):

        if kind=='zoomIn':
            self.zoom += self.zoomStep
            if self.zoom <= self.zoomRange[1]:
                self.scale(self.zoomInFactor, self.zoomInFactor)
            else:
                self.zoom = self.zoomRange[1]
        elif kind=='zoomOut':
            self.zoom -= self.zoomStep
            if self.zoom >= self.zoomRange[0]:
                self.scale(self.zoomOutFactor, self.zoomOutFactor)
            else:
                self.zoom = self.zoomRange[0]

    def toggleCursor(self):

        if self.m_cursor==Qt.BlankCursor:
            self.m_cursor=Qt.ArrowCursor
        else:
            self.m_cursor=Qt.BlankCursor

        self.setCursor(self.m_cursor)
