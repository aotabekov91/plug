import os
import tomli
import inspect
from pathlib import Path
from types import MethodType, BuiltinFunctionType

from plug.utils import Plugman, createFolder

class Plug:

    def __init__(self, *args, **kwargs):

        super().__init__()

        self.files={}
        self.actions={}
        self.running = False
        self.activated = False

        self.kwargs=kwargs
        self.name=kwargs.get('name', None)
        self.config=kwargs.get('config', {})

        self.setup()
        self.initialize()

    def initialize(self): pass

    def setup(self):

        self.setName()
        self.setBasePath()
        self.setFiles()
        self.setSettings()
        self.setActions()

    def setPlugman(self, plugman=Plugman): 

        self.plugman=plugman(self)

    def setActions(self):

        keys=self.config.get('Keys', {})
        for f, k in keys.items():
            m=getattr(self, f, None)
            if m and hasattr(m, '__func__'):
                func=m.__func__
                fname=func.__name__
                n=getattr(m, 'name', fname)
                setattr(func, 'name', n)
                if type(k)==str: 
                    k={'key':k}
                for a, v in k.items():
                    setattr(func, a, v)
                self.actions[(self.name, m.name)]=m 

        # cnd=[MethodType, BuiltinFunctionType]
        for f in self.__dir__():
            m=getattr(self, f)
            # if type(m) in cnd and hasattr(m, 'modes'):
            if hasattr(m, 'modes'):
                d=(self.name, m.name)
                if not d in self.actions:
                    self.actions[d]=m 

    def createFolder(self, 
                     folder=None, 
                     fname='folder'):

        if not folder: 
            name=self.__class__.__name__.lower()
            folder=f'~/{name}'
        path=createFolder(folder)
        setattr(self, fname, path)

    def setName(self):

        if self.name is None: 
            self.name=self.__class__.__name__

    def setBasePath(self):

        file_path=os.path.abspath(
                inspect.getfile(self.__class__))
        self.path=os.path.dirname(
                file_path).replace('\\', '/')

    def setFiles(self):

        for f in os.listdir(self.path):
            path=f'{self.path}/{f}'
            self.files[f]=path
            if f=='config.toml':
                with open(path, 'rb') as y:
                    toml_data=tomli.load(y)
                self.config.update(toml_data)

    def setSettings(self):

        if self.config.get('Settings', None):
            settings=self.config['Settings']
            for name, value in settings.items():
                setattr(self, name, value)

    def run(self):

        self.running=True

    def exit(self):

        self.running=False

    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    def activate(self):

        self.activated=True
        if hasattr(self, 'ui'): 
            self.ui.show()

    def deactivate(self):

        self.activated=False
        if hasattr(self, 'ui'): 
            self.ui.hide()
