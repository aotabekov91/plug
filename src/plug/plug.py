import os
import tomli
import inspect

from plug.utils import Plugman
from plug.utils.plug_utils import createFolder, setKeys

class Plug:

    def __init__(self, *args, **kwargs):

        super().__init__()
        self.files={}
        self.actions={}
        self.kwargs=kwargs
        self.app=kwargs.get('app', None)
        self.name=kwargs.get('name', None)
        self.config=kwargs.get('config', {})
        self.setup()

    def setup(self):

        self.setName()
        self.setBasePath()
        self.setFiles()
        self.setSettings()
        self.setActions()

    def setPlugman(self, plugman=Plugman):
        self.plugman=plugman(app=self)

    def setActions(self):

        def saveSetKeys():

            keys=self.config.get('Keys', {})
            actions=setKeys(self, keys)
            self.actions.update(actions)

        def saveOwnKeys():

            for f in self.__dir__():
                m=getattr(self, f)
                if hasattr(m, 'modes'):
                    d=(self.name, m.name)
                    if not d in self.actions:
                        self.actions[d]=m 

        saveSetKeys()
        saveOwnKeys()

    def createFolder(self, 
                     folder=None, 
                     fname='folder'):

        if not folder: 
            folder=f'~/{self.name.lower()}'
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
