from PyQt5 import QtCore, QtWidgets

class PowerlineWidget(QtWidgets.QWidget):

    def __init__(self):

        super().__init__(objectName='Powerline')
        self.setUI()

    def setUI(self):

        layout=QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.setLayout(layout)
        self.mode=QtWidgets.QLabel(
                objectName='Mode')
        self.info=QtWidgets.QLabel(
                objectName='Info')
        self.detail=QtWidgets.QLabel(
                objectName='Detail')
        self.keys=QtWidgets.QLabel(
                objectName='Keys')
        self.submode=QtWidgets.QLabel(
                objectName='Submode')
        self.model=QtWidgets.QLabel(
                objectName='Model')
        self.index=QtWidgets.QLabel(
                objectName='Index')

        self.mode.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
        self.submode.setAlignment(
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
        self.index.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)

        layout.addWidget(self.mode)
        layout.addWidget(self.submode)
        layout.addStretch(1)
        layout.addWidget(self.info)
        layout.addStretch(1)
        layout.addWidget(self.detail)
        layout.addStretch(100)
        layout.addWidget(
                self.keys, QtCore.Qt.AlignRight)
        # layout.addStretch(1)
        layout.addWidget(
                self.model, QtCore.Qt.AlignRight)
        # layout.addStretch(1)
        layout.addWidget(self.index)
        # layout.addStretch(1)

        self.mode.hide()
        self.info.hide()
        self.detail.hide()
        self.keys.hide()
        self.submode.hide()
        self.model.hide()
        self.index.hide()

    def setText(self, kind, text):

        field=getattr(self, kind, None)
        if field:
            field.setText(text)
            if text:
                field.show()
            else:
                field.hide()
