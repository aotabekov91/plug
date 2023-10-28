import os
from PyQt5 import QtWidgets
from gizmo.utils import register
from plug.qt.plugs.trees.base import TreePlug

class FileBrowser(TreePlug):

    def __init__(
            self, 
            position='dock_left',
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
        self.setModel()
        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)

    def initiate(self):
        self.app.addRender(self)

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

    def setModel(self, path=None):

        m=QtWidgets.QFileSystemModel()
        if path is None: 
            path = os.path.abspath('.')
        m.setRootPath(path)
        idx=m.index(path)
        self.tree.setModel(m)
        self.tree.setRootIndex(idx)
        for i in range(1, 4): 
            self.tree.hideColumn(i)

    def open(self, *args, **kwargs):
        raise

    @register(modes=['run'])
    def openLocalFile(
            self, 
            path, 
            how=None, 
            focus=True
            ):
        self.openFile(path, how, focus)

    @register('o')
    def openFile(
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

    def getLocation(self, encode=True):
        return ''

    def modelId(self):
        return '/'

    def itemId(self):

        idx=self.tree.currentIndex()
        return self.tree.model().filePath(idx)

    def kind(self):
        return 'file'

    def getView(self):
        return self

    def getModel(self, path):

        if os.path.isdir(path):
            if self.app.running:
                self.openModel(path)
            else:
                f=lambda : self.openModel(path)
                self.app.appLaunched.connect(f)
