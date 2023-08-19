from PyQt5 import QtCore, QtWidgets

class StatusWidget(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        layout=QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.mode=QtWidgets.QLabel(objectName='modeLabel')
        self.info=QtWidgets.QLabel()
        self.detail=QtWidgets.QLabel()
        self.model=QtWidgets.QLabel()
        self.page=QtWidgets.QLabel(objectName='pageLabel')

        self.setFixedHeight(20)

        layout.addWidget(self.mode, QtCore.Qt.AlignLeft)
        layout.addStretch(1)
        layout.addWidget(self.info, QtCore.Qt.AlignLeft)
        layout.addStretch(1)
        layout.addWidget(self.detail)
        layout.addStretch(1)
        layout.addWidget(self.model, QtCore.Qt.AlignRight)
        layout.addStretch(1)
        layout.addWidget(self.page, QtCore.Qt.AlignRight)

        self.info.hide()
        self.page.hide()
        self.model.hide()
        self.detail.hide()
