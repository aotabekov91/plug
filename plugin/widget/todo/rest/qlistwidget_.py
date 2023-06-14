import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class CustomListWidget(QListWidget):

    def __init__(self, parent=None):
        super(CustomListWidget, self).__init__(parent)

        self.style_sheet = '''
            QListWidget{
                border-width: 0px;
                color: transparent;
                border-color: transparent; 
                background-color: transparent; 
                }
            QListWidget::item{
                border-style: outset;
                border-width: 0px;
                border-radius: 10px;
                border-style: outset;
                padding: 0px 10px 0px 10px;
                color: transparent;
                border-color: transparent;
                background-color: #101010;
                }
            QListWidget::item:selected {
                border-width: 2px;
                border-color: red;
                }
                '''

        self.setWordWrap(True)
        self.setSpacing(2)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.adjustSize()
        self.setStyleSheet(self.style_sheet)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def sizeHint(self):
        hint=QSize(700, 0)
        if self.count()>0:
            height=0
            for i in range(self.count()):
                item=self.item(0)
                height += item.sizeHint().height()
                if height > 500: break
            hint.setHeight(height+30)
        return hint

class CustomListItem (QWidget):
    def __init__(self, parent=None):
        super(CustomListItem, self).__init__(parent)

        self.style_sheet = '''
            QWidget#containerListItemWidget{
                border-style: outset;
                border-width: 0px;
                border-radius: 10px;
                color: transparent;
                background-color: transparent;
                }
            QWidget#textContainer{
                border-style: outset;
                border-width: 0px;
                border-radius: 10px;
                color: transparent;
                }
            QLabel{
                padding: 0px 0px 0px 0px;
                }
            QLabel#icon{
                padding: 0 0 0 0;
                background-color: transparent;
                }
                '''

        self.textQVBoxLayout = QVBoxLayout()
        self.textQVBoxLayout.setSpacing(0)
        self.textQVBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.textUpQLabel = QLabel()
        self.textUpQLabel.setWordWrap(True)
        self.textDownQLabel = QLabel()
        self.textDownQLabel.setWordWrap(True)
        self.textQVBoxLayout.addWidget(self.textUpQLabel, 50)
        self.textQVBoxLayout.addWidget(self.textDownQLabel, 50)
        self.textQVBoxLayout.addStretch()

        t=QWidget(objectName='textContainer')
        t.setLayout(self.textQVBoxLayout)
        t.setStyleSheet(self.style_sheet)

        self.iconQLabel = QLabel(objectName='icon')
        self.iconQLabel.setFixedWidth(int(0.15*self.size().width()))

        self.allQHBoxLayout = QHBoxLayout()
        self.allQHBoxLayout.addWidget(self.iconQLabel)
        self.allQHBoxLayout.addWidget(t)

        s=QWidget(objectName='containerListItemWidget')
        s.setStyleSheet(self.style_sheet)
        s.setLayout(self.allQHBoxLayout)

        layout=QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(s)

        self.setLayout(layout)

        self.textUpQLabel.hide()
        self.textDownQLabel.hide()
        self.iconQLabel.hide()

    def setTextDown(self, text):
        self.textDownQLabel.setText(str(text))
        self.textDownQLabel.show()
        self.adjustSize()

    def setTextUp(self, text):
        self.textUpQLabel.setText(str(text))
        self.textUpQLabel.show()
        self.adjustSize()

    def setIcon(self, imagePath):
        self.iconQLabel.path = imagePath
        if os.path.isfile(imagePath):
            scale=self.iconQLabel.size()
            w, h=scale.width(), scale.height()
            self.iconQLabel.setPixmap(QPixmap(imagePath).scaled(w, h, Qt.KeepAspectRatio))
            self.iconQLabel.show()

    def adjustSize(self):
        self.textUpQLabel.adjustSize()
        self.textDownQLabel.adjustSize()

    def sizeHint(self):
        self.adjustSize()
        size=self.textUpQLabel.size()
        if self.textDownQLabel.isVisible():
            s=self.textDownQLabel.size()
            size.setHeight(size.height()+s.height())
        size.setHeight(size.height()+40)
        if size.height()<80:
            size.setHeight(80)
        return size
