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
                'FileBrowser': '<c-.>'
                }, 
            keywords=['files'],
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

    def initiate(self):
        self.app.addRender(self)

    def getModel(self, path):

        if os.path.isdir(path):
            if self.app.running:
                self.openModel(path)
            else:
                f=lambda : self.openModel(path)
                self.app.appLaunched.connect(f)

    def openModel(self, path):

        m=self.tree.model()
        idx=m.index(path)
        p=idx.parent()
        ppath=m.filePath(p)
        m.setRootPath(ppath)
        self.tree.setRootIndex(p)
        self.tree.setCurrentIndex(idx)
        self.activate()
        self.ui.dock.toggleFullscreen()

    def on_plugsLoaded(self, plugs):

        runlist=plugs.get('RunList', None)
        if runlist:
            runlist.setArgOptions(
                'openFile', 'path', 'path')

    def getPath(self, index=None):

        if not index: 
            index=self.tree.currentIndex()
        if index:
            model=self.tree.model()
            path=model.filePath(index)
            if os.path.exists(path): 
                return path

    def setPath(self, path=None):

        model=QFileSystemModel()
        if path is None: 
            path = os.path.abspath('.')
        model.setRootPath(path)
        idx=model.index(path)
        self.tree.setModel(model)
        self.tree.setRootIndex(idx)
        for i in range(1, 4): 
            self.tree.hideColumn(i)

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

        if not path:
            idx=self.tree.currentIndex()
            path=self.getPath(idx)
        if path:
            if os.path.isdir(path): 
                idx=self.tree.currentIndex()
                self.tree.expand(idx)
            else:
                self.app.open(
                        path, 
                        how=how, 
                        focus=focus)
            super().open(how, focus)
