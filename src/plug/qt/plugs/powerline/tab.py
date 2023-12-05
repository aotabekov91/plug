from PyQt5 import QtCore, QtWidgets, QtGui

class Tabber(QtCore.QObject):

    def __init__(
            self, 
            toolbar=None,
            objectName='TabWidget',
            **kwargs
            ):

        super().__init__(
                parent=toolbar,
                objectName=objectName,
                **kwargs)
            
        self.toolbar=toolbar

    def clear(self):

        l=self.toolbar.layout()
        i=l.takeAt(0)
        while not i is None:
            w=i.widget()
            if w:
                w.setParent(None)
                w.hide()
            i=l.takeAt(0)

    def setTabs(self, v):

        self.clear()
        if not v.check('hasTabber'):
            self.toolbar.hide()
            return
        t=v.m_tabber
        if t.count()<2:
            self.toolbar.hide()
            return
        cidx=t.currentIndex()
        for i in range(t.count()):
            w=t.widget(i)
            name=w.m_tab_name
            oname='Tab'
            if name==w.m_tab_idx:
                name=f'[{name+1}]'
            if cidx==w.m_tab_idx: 
                name=f'{name}*'
                oname='CurrentTab'
            l=QtWidgets.QLabel(str(name))
            l.setObjectName(oname)
            l.setSizePolicy(
                    QtWidgets.QSizePolicy.Expanding, 
                    QtWidgets.QSizePolicy.Maximum)
            l.setContentsMargins(0,0,0,0)
            l.setAlignment(
                QtCore.Qt.AlignCenter|
                QtCore.Qt.AlignVCenter)
            self.toolbar.addWidget(l)
        self.toolbar.show()
