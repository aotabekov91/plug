import os
from PyQt5 import QtWidgets
from gizmo.utils import register
from plug.qt.plugs.trees.base import TreePlug

class FileView(TreePlug):

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
        self.app.addRender(self)

        super().__init__(
                position=position,
                keywords=keywords,
                prefix_keys=prefix_keys,
                **kwargs)
        self.setModel()
        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)

    def openModel(
            self, 
            path, 
            fullscreen=False
            ):

        m=self.tree.model()
        idx=m.index(path)
        p=idx.parent()
        self.tree.setRootIndex(p)
        self.tree.setCurrentIndex(idx)
        self.activate()
        if fullscreen:
            self.ui.dock.toggleFullscreen()


    def getPath(self, index=None):

        if not index: 
            index=self.tree.currentIndex()
        if index:
            model=self.tree.model()
            path=model.filePath(index)
            if os.path.exists(path): 
                return path

    def setModel(
            self, 
            root_path='/',
            path = os.path.abspath('.')
            ):

        m=QtWidgets.QFileSystemModel()
        m.setRootPath(root_path)
        idx=m.index(path)
        self.tree.setModel(m)
        self.tree.setRootIndex(idx)
        for i in range(1, 4): 
            self.tree.hideColumn(i)

    def open(self, *args, **kwargs):

        pos=kwargs.get('position', None)
        if pos: self.openModel(pos)

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
        return self.itemId()

    def model(self):
        return self

    def modelId(self):
        return ''

    def element(self):
        pass

    def kind(self):
        return 'file'

    def getView(self):
        return self

    def itemId(self):

        idx=self.tree.currentIndex()
        return self.tree.model().filePath(idx)

    def getModel(self, path):

        if os.path.isdir(path):
            if self.app.running:
                self.openModel(path)
            else:
                f=lambda : self.openModel(path, True)
                self.app.appLaunched.connect(f)
