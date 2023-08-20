from PyQt5 import QtCore, QtWidgets

class StatusWidget(QtWidgets.QWidget):

    def __init__(self):

        super().__init__(objectName='Powerline')

        layout=QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.mode=QtWidgets.QLabel(
                objectName='Powerline_mode')
        self.info=QtWidgets.QLabel(
                objectName='Powerline_mnfo')
        self.detail=QtWidgets.QLabel(
                objectName='Powerline_detail')
        self.model=QtWidgets.QLabel(
                objectName='Powerline_model')
        self.keys=QtWidgets.QLabel(
                objectName='Powerline_keys')
        self.page=QtWidgets.QLabel(
                objectName='Powerline_page')

        layout.addWidget(self.mode, QtCore.Qt.AlignLeft)
        layout.addStretch(1)
        layout.addWidget(self.info, QtCore.Qt.AlignLeft)
        layout.addStretch(1)
        layout.addWidget(self.detail)
        layout.addStretch(10)
        layout.addWidget(self.model, QtCore.Qt.AlignRight)
        layout.addStretch(1)
        layout.addWidget(self.keys, QtCore.Qt.AlignRight)
        layout.addStretch(1)
        layout.addWidget(self.page)

        self.setFixedHeight(20)

        self.info.hide()
        self.page.hide()
        self.model.hide()
        self.detail.hide()

    def setText(self, kind, text):

        field=getattr(self, kind, None)
        if field:
            field.show()
            field.setText(text)
