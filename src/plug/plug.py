import os
import tomli
import inspect

from pathlib import Path
from types import MethodType, BuiltinFunctionType

from plug.utils import Plugman

class Plug:

    def __init__(self, *args, **kwargs):

        super().__init__()

        self.files={}
        self.actions={}
        self.commandKeys={}
        self.running = False
        self.activated = False

        self.kwargs=kwargs
        self.name=kwargs.get('name', None)
        self.config=kwargs.get('config', None)

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

    def setActions(self, obj=None):

        if self.config.get('Keys'):
            keys=self.config['Keys']
            for f, key in keys.items():
                m=getattr(self, f, None)
                if m and hasattr(m, '__func__'):
                    if type(key)==str:
                        modes=getattr(m, 'modes', ['command'])
                        setattr(m.__func__, 'key', f'{key}')
                    elif 'key' in key:
                        modes=getattr(m, 'modes', ['command'])
                        modes=key.get('modes', modes)
                        key=key.get('key')
                    f=getattr(m, 'name', m.__func__.__name__)
                    setattr(m.__func__, 'name', f)
                    setattr(m.__func__, 'modes', modes)
                    d=(self.__class__.__name__, m.name)
                    self.actions[d]=m 
                    self.commandKeys[m.key]=m
        if not obj: obj=self
        cnd=[MethodType, BuiltinFunctionType]
        for f in obj.__dir__():
            m=getattr(obj, f)
            if type(m) in cnd and hasattr(m, 'modes'):
                name=getattr(obj, 
                             'name', 
                             obj.__class__.__name__)
                d=(name, m.name)
                if not d in self.actions:
                    self.actions[d]=m 
                    if type(m.key)==str:
                        self.commandKeys[m.key]=m
                    elif type(m.key)==list:
                        for k in m.key: 
                            self.commandKeys[k]=m

    def createFolder(self, 
                     folder=None, 
                     fname='folder'):

        if not folder: 
            name=self.__class__.__name__.lower()
            folder=f'~/{name}'
        folder=os.path.expanduser(folder)
        attr=Path(folder)
        setattr(self, fname, attr)
        if not os.path.exists(folder): 
            attr.mkdir(parents=True, exist_ok=True)

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
        if hasattr(self, 'ui'): self.ui.show()

    def deactivate(self):

        self.activated=False
        if hasattr(self, 'ui'): self.ui.hide()
