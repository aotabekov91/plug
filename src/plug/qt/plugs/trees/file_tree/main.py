import os
from PyQt5.QtWidgets import QFileSystemModel

from gizmo.utils import register
from plug.qt.plugs.trees.base import TreePlug

class FileBrowser(TreePlug):

    def __init__(
            self, 
            position='left',
            prefix_keys={
                'command': 'f', 
                'FileBrowser': '<c-u>'
                }, 
            keywords=['files', 'file browser'], 
            **kwargs
            ):

        super().__init__(
                position=position,
                keywords=keywords,
                prefix_keys=prefix_keys,
                **kwargs)
        self.setPath()
        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)

    def on_plugsLoaded(self, plugs):

        runlist=plugs.get('RunList', None)
        if runlist:
            runlist.setArgOptions(
                'openFile', 'path', 'path')

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

    @register(modes=['run'])
    def openFile(
            self, 
            path, 
            how=None, 
            focus=True
            ):
        self.open(path, how, focus)

    @register('o')
    def open(
            self, 
            path=None, 
            how=None, 
            focus=False
            ):

        tree=self.ui.main.tree
        if not path:
            index=tree.currentIndex()
            path=self.getPath(index)
        if path:
            if os.path.isdir(path): 
                tree.expand(tree.currentIndex())
            else:
                self.app.open(
                        path, 
                        how=how, 
                        focus=focus,
                        )
            super().open(how, focus)
