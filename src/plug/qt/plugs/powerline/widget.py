from PyQt6 import QtCore, QtWidgets

class PowerlineWidget(QtWidgets.QWidget):

    def __init__(self):

        super().__init__(objectName='Powerline')

        layout=QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.mode=QtWidgets.QLabel(
                objectName='Mode')
        self.info=QtWidgets.QLabel(
                objectName='Info')
        self.detail=QtWidgets.QLabel(
                objectName='Detail')
        self.model=QtWidgets.QLabel(
                objectName='Model')
        self.keys=QtWidgets.QLabel(
                objectName='Keys')
        self.page=QtWidgets.QLabel(
                objectName='Page')

        self.mode.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
        self.info.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
        self.detail.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
        self.keys.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
        self.page.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)

        layout.addWidget(self.mode, QtCore.Qt.AlignLeft)
        layout.addStretch(1)
        layout.addWidget(self.info, QtCore.Qt.AlignLeft)
        layout.addStretch(1)
        layout.addWidget(self.detail)
        layout.addStretch(100)
        layout.addWidget(self.keys, QtCore.Qt.AlignRight)
        layout.addStretch(1)
        layout.addWidget(self.model, QtCore.Qt.AlignRight)
        layout.addStretch(1)
        layout.addWidget(self.page)
        layout.addStretch(1)

        # self.setFixedHeight(20)

        self.info.hide()
        self.page.hide()
        self.model.hide()
        self.detail.hide()

    def setText(self, kind, text):

        field=getattr(self, kind, None)
        if field:
            field.show()
            field.setText(text)
