import os
from gizmo.utils import register
from gizmo.widget import TreeWidget
from plug.qt.plugs.viewer import Viewer
from PyQt5.QtWidgets import QFileSystemModel

class FileBrowser(Viewer):

    def __init__(
            self, 
            position='dock_left',
            leader_keys={
                'command': 'f', 
                'FileBrowser': '<c-.>'
                }, 
            keywords=['files'],
            **kwargs
            ):

        super().__init__(
                position=position,
                keywords=keywords,
                leader_keys=leader_keys,
                **kwargs)
        self.setUI()
        self.connect()

    def connect(self):

        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)

    def on_plugsLoaded(self, plugs):

        rplug=plugs.get('RunList', None)
        if rplug:
            rplug.setArgOptions(
                'openFile', 'path', 'path')

    def setUI(self):

        tree=TreeWidget()
        self.uiman.setUI(tree)
        self.setModel()

    def getPath(self, index=None):

        if not index: 
            index=self.ui.currentIndex()
        if index:
            model=self.ui.model()
            path=model.filePath(index)
            if os.path.exists(path): 
                return path

    def setModel(
            self, 
            root='/',
            path = None,
            ):

        m_model=QFileSystemModel()
        m_model.setRootPath(root)
        self.m_model=m_model
        if not path:
            path = os.path.abspath('.')
        idx=m_model.index(path)
        self.ui.setModel(m_model)
        self.ui.setRootIndex(idx)
        for i in range(1, 4): 
            self.ui.hideColumn(i)

    def open(self, source=None, **kwargs):

        pos=kwargs.get('position', None)
        path = pos or source
        if self.app.running:
            self._open(path)
        else:
            f=lambda : self._open(path, True)
            self.app.appLaunched.connect(f)

    def _open(
            self, 
            path, 
            fullscreen=False,
            ):

        m=self.ui.model()
        idx=m.index(path)
        p=idx.parent()
        self.ui.setRootIndex(p)
        self.ui.setCurrentIndex(idx)
        self.activate()
        if fullscreen:
            self.ui.dock.toggleFullscreen()

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
            idx=self.ui.currentIndex()
            path=self.getPath(idx)
        if path:
            if os.path.isdir(path): 
                idx=self.ui.currentIndex()
                self.ui.expand(idx)
            else:
                self.app.open(
                        path, 
                        how=how, 
                        focus=focus)
                self.listen()
            # super().open(how, focus)

    def getLocation(self, encode=True):
        return self.itemId()

    def itemId(self):

        idx=self.ui.currentIndex()
        return self.ui.model().filePath(idx)

    def model(self):
        return self.m_model

    def modelId(self):
        return ''

    def getView(self):
        return self

    def kind(self):
        return 'file'

    def element(self, idx):

        if not idx: 
            index=self.tree.currentIndex()
        if index:
            model=self.tree.model()
            path=model.filePath(index)
            if os.path.exists(path): 
                return path

    def isCompatible(self, source):

        if source:
            return os.path.isdir(source)
