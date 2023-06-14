from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class List(QListWidget):

    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)

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

        self.setStyleSheet(self.style_sheet)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
