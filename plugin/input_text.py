from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class InputWidget(QPlainTextEdit):

    returnPressed=pyqtSignal()

    def __init__ (self, *args, **kwargs): 

        super().__init__(*args, **kwargs) 

        self.style_sheet='''
            QLineEdit{
                color: black;
                background-color: white;
                border-color: red;
                border-width: 2px;
                border-radius: 10px;
                border-style: outset;
                padding: 0 0 0 10px;
                }
                '''

        self.setStyleSheet(self.style_sheet)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.textChanged.connect(self.adjustSize)

    def sizeHint(self):
        size=self.document().size()
        width=int(size.width())
        if size.height()==1.0: 
            times=int(width/self.size().width())
        else:
            times=size.height()
        if times==0: times=1
        height=int(25*times)
        if height<50: height=50
        size=QSize(width, height)
        return size

    def text(self): return self.toPlainText()

    def event(self, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                self.returnPressed.emit()
                event.accept()
                return True
        return super().event(event)
