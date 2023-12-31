from PyQt5 import QtCore, QtWidgets

class StatusWidget(QtWidgets.QWidget):

    def __init__(self):

        super().__init__(
                objectName='Powerline')
        self.setupUI()

    def setupUI(self):

        self.mode=QtWidgets.QLabel(
                objectName='ModeName')
        self.submode=QtWidgets.QLabel(
                objectName='SubmodeName')
        self.info=QtWidgets.QLabel(
                objectName='InfoName')
        self.detail=QtWidgets.QLabel(
                objectName='DetailName')
        self.keys=QtWidgets.QLabel(
                objectName='KeysName')
        self.type=QtWidgets.QLabel(
                objectName='TypeName')
        self.model=QtWidgets.QLabel(
                objectName='ModelName')
        self.view=QtWidgets.QLabel(
                objectName='ViewName')
        self.index=QtWidgets.QLabel(
                objectName='IndexName')
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
