from PyQt5 import QtWidgets

class TabWidget(QtWidgets.QWidget):

    def __init__(
            self, 
            *args, 
            objectName='TabWidget',
            **kwargs
            ):

        super().__init__(
                *args,
                objectName=objectName,
                **kwargs)
        self.setup()

    def setup(self):

        self.m_layout=QtWidgets.QHBoxLayout()
        self.m_layout.setContentsMargins(0,0,0,0)
        self.m_layout.setSpacing(5)
        self.setLayout(self.m_layout)

    def clear(self):

        item=self.m_layout.takeAt(0)
        while not item is None:
            w=item.widget()
            if w:
                w.setParent(None)
                w.hide()
            item=self.m_layout.takeAt(0)

    def setTabs(self, v):

        self.clear()
        if not v.check('hasTabber'):
            self.hide()
            return
        t=v.m_tabber
        if t.count()<2:
            self.hide()
            return
        cidx=t.currentIndex()
        self.m_layout.addStretch(10)
        for i in range(t.count()):
            w=t.widget(i)
            name=w.m_tab_name
            oname=''
            if name==w.m_tab_idx:
                name=f'[{name+1}]'
            if cidx==w.m_tab_idx: 
                name=f'{name}*'
                oname='test'
            # l=w.m_tab_label.setText(str(name))
            l=QtWidgets.QLabel(str(name))
            l.setObjectName(oname)
            self.m_layout.addWidget(l)
        self.m_layout.addStretch(10)
        l=QtWidgets.QLabel(str(t.name))
        self.m_layout.addWidget(l)
        self.show()
