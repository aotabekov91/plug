from PyQt5 import QtWidgets

from plug.qt import Plug
from gizmo.utils import register
from gizmo.widget import InputTree

class TreePlug(Plug):

    def __init__(
            self, 
            *args, 
            **kwargs
            ):

        self.follow_index=True
        super().__init__(
                *args, 
                **kwargs
                )
        self.setUI()

    def setUI(self):

        self.uiman.setUI()
        ui=InputTree()
        self.ui.addWidget(
                ui, 'main', main=True)
        ui.tree.setSelectionBehavior(
                QtWidgets.QAbstractItemView.SelectRows)
        ui.tree.itemChanged.connect(
                self.on_itemChanged)
        ui.tree.expanded.connect(
                self.on_outlineExpanded)
        ui.tree.openWanted.connect(
                self.on_outlineClicked)
        ui.tree.indexChanged.connect(
                self.on_indexChanged)
        ui.tree.collapsed.connect(
                self.on_outlineCollapsed)
        ui.tree.returnPressed.connect(
                self.on_outlineClicked)
        ui.tree.clicked.connect(
                self.on_outlineClicked)

    @register('i')
    def openBelow(self): 
        self.open(how='below', focus=False)

    @register('O')
    def openReset(self): 
        self.open(how='reset', focus=False)

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

    def setData(self): 
        pass

    def on_outlineCollapsed(self, index): 
        pass

    def on_outlineExpanded(self, index): 
        pass

    def on_outlineClicked(self, index): 
        pass

    def on_indexChanged(self, index): 
        pass

    def on_itemChanged(self, item):
        pass

    def on_viewChanged(self, view, prev): 
        self.setData()

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
