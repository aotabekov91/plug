from PyQt5 import QtCore, QtWidgets

class PowerlineWidget(QtWidgets.QWidget):

    def __init__(self):

        super().__init__(
                objectName='Powerline')
        self.setupUI()

    def setupUI(self):

        self.mode=QtWidgets.QLabel(
                objectName='Mode')
        self.submode=QtWidgets.QLabel(
                objectName='Submode')
        self.info=QtWidgets.QLabel(
                objectName='Info')
        self.detail=QtWidgets.QLabel(
                objectName='Detail')
        self.keys=QtWidgets.QLabel(
                objectName='Keys')
        self.type=QtWidgets.QLabel(
                objectName='Type')
        self.model=QtWidgets.QLabel(
                objectName='Model')
        self.view=QtWidgets.QLabel(
                objectName='View')
        self.index=QtWidgets.QLabel(
                objectName='Index')
        self.mode.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
        self.submode.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
        self.type.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
        self.info.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
        self.detail.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
        self.view.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
        self.keys.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
        self.index.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
        l=QtWidgets.QHBoxLayout()
        l.setSpacing(0)
        l.setContentsMargins(0,0,0,0)
        l.addWidget(self.mode)
        l.addWidget(self.submode)
        l.addWidget(self.type)
        l.addStretch(1)
        l.addWidget(self.info)
        l.addStretch(1)
        l.addWidget(self.detail)
        l.addStretch(100)
        ar=QtCore.Qt.AlignRight
        l.addWidget(self.keys, ar)
        l.addWidget(self.model, ar)
        l.addWidget(self.view, ar)
        l.addWidget(self.index)
        self.setLayout(l)
        self.mode.hide()
        self.info.hide()
        self.view.hide()
        self.keys.hide()
        self.type.hide()
        self.model.hide()
        self.index.hide()
        self.detail.hide()
        self.submode.hide()

    def setText(self, kind, text):

        f=getattr(self, kind, None)
        if f:
            f.setText(str(text))
            if text is None:
                return f.hide()
            return f.show()
