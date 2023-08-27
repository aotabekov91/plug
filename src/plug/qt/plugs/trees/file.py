import os

from PyQt5.QtWidgets import QFileSystemModel

from .base import TreePlug

class FileBrowser(TreePlug):

    def __init__(self, 
                 mode_keys={'command': 'f'},
                 **kwargs):

        super().__init__(
                mode_keys=mode_keys,
                **kwargs)
        self.setPath()

    def getPath(self, index=None):

        tree=self.ui.main.tree
        if not index: 
            index=tree.currentIndex()
        if index:
            model=tree.model()
            path=model.filePath(index)
            if os.path.exists(path): 
                return path

    def setPath(self, path=None):

        tree=self.ui.main.tree
        tree.setModel(QFileSystemModel())
        if path is None: 
            path = os.path.abspath('.')
        tree.model().setRootPath(path)
        index=tree.model().index(path)
        tree.setRootIndex(index)

        for i in range(1, 4): 
            self.ui.main.tree.hideColumn(i)

    def open(self, how='reset', focus=True):

        tree=self.ui.main.tree
        index=tree.currentIndex()
        path=self.getPath(index)
        if path:
            if os.path.isdir(path): 
                tree.expand(tree.currentIndex())
            else:
                self.app.window.main.open(
                        path, 
                        how=how, 
                        focus=focus)
            super().open(how, focus)
