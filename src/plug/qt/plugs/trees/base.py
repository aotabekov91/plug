from PyQt5 import QtWidgets

from plug.qt import Plug
from gizmo.utils import register
from gizmo.widget import InputTree

class TreePlug(Plug):

    def __init__(self, *args, **kwargs):

        self.follow_index=True
        super().__init__(*args, **kwargs)

    def setup(self):

        super().setup()
        self.setUI()

    def setUI(self):

        self.uiman.setUI()
        input_tree=InputTree(set_base_style=False)
        input_tree.tree.setSelectionBehavior(
                QtWidgets.QAbstractItemView.SelectRows)
        self.ui.addWidget(
                input_tree, 'main', main=True)
        self.ui.main.tree.clicked.connect(
                self.on_outlineClicked)
        self.ui.main.tree.itemChanged.connect(
                self.on_itemChanged)
        self.ui.main.tree.expanded.connect(
                self.on_outlineExpanded)
        self.ui.main.tree.openWanted.connect(
                self.on_outlineClicked)
        self.ui.main.tree.indexChanged.connect(
                self.on_indexChanged)
        self.ui.main.tree.collapsed.connect(
                self.on_outlineCollapsed)
        self.ui.main.tree.returnPressed.connect(
                self.on_outlineClicked)
        self.ui.installEventFilter(self)

    @register('t', modes=['command'])
    def toggle(self): super().toggle()

    @register('i')
    def openBelow(self): 

        self.open(how='below', focus=False)
        self.ui.show()

    @register('O')
    def openReset(self): 

        self.open(how='reset', focus=False)
        self.ui.show()

    @register('s')
    def center(self):

        if not self.follow_index:
            self.follow_index=True
            self.ui.main.tree.indexChanged.disconnect(
                    self.on_outlineClicked)
        else:
            self.follow_index=False
            self.ui.main.tree.indexChanged.connect(
                    self.on_outlineClicked)

    def open(self, how, focus, *args, **kwargs): 

        if focus:
            self.delistenWanted.emit()
        else:
            self.ui.show()

    def on_outlineCollapsed(self, index): pass

    def on_outlineExpanded(self, index): pass

    def on_outlineClicked(self, index=None): pass

    def setData(self): pass

    def on_indexChanged(self, index): pass

    def on_itemChanged(self, item): pass

    def on_viewChanged(self, view, prev): self.setData()

    def find(self, item, model, parent=None):

        root=model.invisibleRootItem()

        if root.rowCount()>0: 
            if not parent: 
                parent=model.indexFromItem(root.child(0,0))

            for row in range(model.rowCount(parent)):
                index=model.index(row, 0, parent)
                if index==model.indexFromItem(item): 
                    return index

            for row in range(model.rowCount(parent)):
                index=model.index(row, 0, parent)
                match=self.sync(item, model, index)
                if match.isValid(): return match
            if root.rowCount()>0:
                return model.indexFromItem(root.child(0,0))
