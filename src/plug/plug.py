import os
import tomli
from inspect import getfile
from plug.utils import setKeys, createFolder

class Plug:

    def __init__(
            self, 
            *args, 
            **kwargs
            ):

        super().__init__()
        self.files={}
        self.actions={}
        self.kwargs=kwargs
        self.app=kwargs.get(
                'app', None)
        self.name=kwargs.get(
                'name', None)
        self.config=kwargs.get(
                'config', {})
        self.setup()
        self.initiate()

    def initiate(self):
        pass

    def setup(self):

        self.setName()
        self.setBasePath()
        self.setFiles()
        self.setSettings()
        self.setActions()

    def setModer(self, moder, **kwargs):

        config=self.config.get(
                'Moder', {})
        self.moder=moder(
                app=self,
                config=config,
                **kwargs,
                )

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

    def createFolder(
            self, 
            folder=None, 
            fname='folder'
            ):
        
        if not folder: 
            folder=f'~/{self.name.lower()}'
        p=createFolder(folder)
        setattr(self, fname, p)

    def setName(self):

        if self.name is None: 
            self.name=self.__class__.__name__

    def setBasePath(self):

        p=os.path.abspath(
                getfile(self.__class__))
        self.path=os.path.dirname(
                p).replace('\\', '/')

    def setFiles(self):

        for f in os.listdir(self.path):
            path=f'{self.path}/{f}'
            self.files[f]=path
            if f=='config.toml':
                with open(path, 'rb') as y:
                    print(path)
                    toml_data=tomli.load(y)
                self.config.update(toml_data)

    def setSettings(self):

        s=self.config.get('Settings', {})
        for n, v in s.items():
            setattr(self, n, v)
