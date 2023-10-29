import os
from PyQt5 import QtWidgets

class FileModel(QtWidgets.QFileSystemModel):

    def element(self, idx=None):

        if not idx: 
            index=self.tree.currentIndex()
        if index:
            model=self.tree.model()
            path=model.filePath(index)
            if os.path.exists(path): 
                return path

    def id(self):
        return ''

    def kind(self):
        return 'file'
