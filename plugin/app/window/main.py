from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..docks import Docks
from ..display import Display
from ..plugin import Configure
from ..statusbar import StatusBar

class MainWindow(QMainWindow):

    viewCreated=pyqtSignal(object)
    
    def __init__(self, app):

        super().__init__()

        self.app=app
        self.configure=Configure(app, 'Window', self)

        self.setUI()

    def setUI(self):

        # Order matters
        self.display=Display(self.app, self)
        self.display.viewCreated.connect(self.viewCreated)

        self.docks=Docks(self)
        self.bar=StatusBar(self)

        self.setStatusBar(self.bar)
        self.setCentralWidget(self.display)

        stl='''
            QWidget {
                color: white;
                border-color: transparent;
                background-color: transparent;
                }
               ''' 
        self.setStyleSheet(stl)
        self.setAcceptDrops(True)
        self.setContentsMargins(2, 2, 2, 2)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()

    def close(self): self.app.exit()

    def open(self, filePath): 

        data=self.app.buffer.load(filePath)
        self.display.open(data)
