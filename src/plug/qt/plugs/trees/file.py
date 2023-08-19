import os

from PyQt5.QtWidgets import QFileSystemModel

from .base import TreePlug

class FileBrowser(TreePlug):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.setPath()

    def getPath(self, index=None):

        if not index: index=self.ui.main.tree.currentIndex()

        if index:
            path=self.ui.main.tree.model().filePath(index)
            if os.path.exists(path): return path

    def setPath(self, path=None):

        self.ui.main.tree.setModel(QFileSystemModel())
        if path is None: path = os.path.abspath('.')
        self.ui.main.tree.model().setRootPath(path)
        index=self.ui.main.tree.model().index(path)
        self.ui.main.tree.setRootIndex(index)

        for i in range(1, 4): self.ui.main.tree.hideColumn(i)

    def open(self, how='reset', focus=True):

        index=self.ui.main.tree.currentIndex()
        path=self.getPath(index)
        if path:
            if os.path.isdir(path): 
                self.ui.main.tree.expand(
                        self.ui.main.tree.currentIndex())
            else:
                self.app.window.main.open(path, how=how, focus=focus)
            super().open(how, focus)
