from plug.qt import Plug
from gizmo.utils import tag
from PyQt5 import QtCore, QtWidgets

class Tabline(Plug):

    prefix_keys={'normal': '<c-t>'}

    def event_functor(self, e, ear):

        x=[QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]
        if e.key() in x:
            self.rename()
            self.octivate()

    @tag('t', modes=['normal'])
    def activateTabs(self):

        if not self.current: return
        if self.m_tabs.isVisible():
            self.m_tabs.hide()
        else:
            self.m_tabs.show()

    def rename(self):

        w=self.rename_widget
        if self.current and w:
            n=self.app.ui.bar.edit.text()
            w.m_tab_name=n
            self.updateTabLine(t=self.current)

    @tag('r', modes=['normal'])
    def activateRename(self, digit=None):

        if self.current:
            idx=self.current.currentIndex()
            if digit: idx=digit-1
            self.activate()
            self.setSubmode('rename')
            w=self.current.widget(idx)
            self.rename_widget=w
            self.app.ui.bar.activateBottom(
                    edit=w.m_tab_name)

    def octivate(self):

        super().octivate()
        self.rename_widget=None
        self.app.ui.bar.octivateBottom()

    def setup(self):

        super().setup()
        self.tabs={}
        self.setTabLine()
        self.current=None
        self.rename_widget=None
        self.app.handler.viewChanged.connect(
                self.updateTabLine)
        self.app.handler.viewCreated.connect(
                self.setTabberWidget)
        self.setTabberWidget(self.app.display)

    def setTabberWidget(self, v):

        t=None
        if self.checkProp('hasTabs', v):
            t=v
        elif self.checkProp('m_tabber', v):
            t=v.m_tabber
        if t:
            w=QtWidgets.QWidget()
            l=QtWidgets.QHBoxLayout(w)
            l.setContentsMargins(0,0,0,0)
            l.setSpacing(0)
            w.setLayout(l)
            self.tabs[t]=w

    def setTabLine(self):

        b=self.app.ui.bar
        t=QtWidgets.QWidget(objectName='Tabs')
        l=QtWidgets.QHBoxLayout(t)
        b.clayout.addWidget(t)
        l.setContentsMargins(0,0,0,0)
        l.setSpacing(0)
        t.setLayout(l)
        self.m_tabs=t

    def clearLayout(self, l):

        i=l.takeAt(0)
        while not i is None:
            w=i.widget()
            if w:
                w.setParent(None)
                w.hide()
            i=l.takeAt(0)

    def updateTabLine(self, v=None, t=None):

        if not t:
            t=getattr(v, 'm_tabber', None)
        self.current=t
        if not t: return 
        ll=self.m_tabs.layout()
        self.clearLayout(ll)
        self.m_tabs.hide()
        tw=self.tabs.get(t)
        if not tw: 
            self.setTabberWidget(t)
        tw=self.tabs.get(t)
        tl=tw.layout()
        idx=t.currentIndex()
        self.clearLayout(tl)
        for i in range(t.count()):
            oname='Tab'
            w=t.widget(i)
            widx=w.m_tab_idx
            name=w.m_tab_name
            if name==w.m_tab_idx:
                name=f'[{name+1}]'
            else:
                name=f'{name} [{widx+1}]'
            if idx==w.m_tab_idx: 
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
            tl.addWidget(l)
        ll.addWidget(tw)
        tw.show()
        if t.count()<2:
            self.m_tabs.hide()
        else:
            self.m_tabs.show()
