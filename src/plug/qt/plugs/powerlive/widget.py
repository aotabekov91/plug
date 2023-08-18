from PyQt5 import QtCore, QtWidgets

class StatusWidget(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        self.style_sheet='''
            QLabel{
                background-color: red;
                }
                '''

        layout=QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.mode=QtWidgets.QLabel()
        self.info=QtWidgets.QLabel()
        self.edit=QtWidgets.QLineEdit(self)
        self.detail=QtWidgets.QLabel()
        self.model=QtWidgets.QLabel()
        self.page=QtWidgets.QLabel()

        self.setFixedHeight(25)

        self.layout.addWidget(self.mode, 1)
        self.layout.addWidget(self.info, 100)
        self.layout.addWidget(self.edit, 100)
        self.layout.addWidget(self.detail)
        self.layout.addWidget(self.model)
        self.layout.addWidget(self.page, 0)

        self.info.hide()
        self.edit.hide()
        self.detail.hide()

        self.setSizeGripEnabled(False)
        self.setStyleSheet(self.style_sheet)
