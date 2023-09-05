import re

from plug.qt import PlugObj
from plug.qt.utils import register

class Colorscheme(PlugObj):

    def __init__(self, 
            *args, 
            file_name='style.css',
            **kwargs):

        self.colorschemes={}
        self.file_name=file_name
        self.colorscheme='default'

        super().__init__(*args, **kwargs)

        self.app.plugman.plugsLoaded.connect(
                self.on_plugsLoaded)

    def readStyleSheet(self, path):

        with open(path, 'r') as y:
            lines=' '.join(y.readlines())
            return re.sub(r'[\n\t]', ' ', lines)

    def on_plugsLoaded(self, plugs):

        default=''
        for name, plug in plugs.items():
            if hasattr(plug, 'ui'):
                default+=plug.ui.styleSheet()
            path=plug.files.get(self.file_name, None)
            if path:
                default+=self.readStyleSheet(path)

        path=self.app.files.get(self.file_name, None)
        if path:
            default+=self.readStyleSheet(path)

        self.colorschemes['default']=default
        self.setColorscheme(self.colorscheme)

    def setColorscheme(self, colorscheme):
        
        style_sheet=self.colorschemes.get(
                colorscheme, None)
        if style_sheet:
            self.app.setStyleSheet(style_sheet)
