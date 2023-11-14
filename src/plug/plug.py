import os
import tomli
from inspect import getfile
from plug.utils import setKeys, createFolder, Moder

class Plug:

    main_app=False

    def __init__(
            self, 
            *args,
            app=None,
            name=None,
            config={},
            **kwargs):

        super().__init__()
        self.app=app
        self.files={}
        self.name=name
        self.renders=[]
        self.actions={}
        self.functions={}
        self.config=config
        self.kwargs=kwargs
        self.setup()

    def addRender(self, render):
        self.renders+=[render]

    def setup(self):

        self.setName()
        self.setBasePath()
        self.setFiles()
        self.setSettings()
        self.updateArgs()
        self.setActions()
        if self.main_app:
            self.app=self
            self.setModer()

    def updateArgs(self):

        settings=self.config.get(
                'Settings', {})
        for n, s in settings.items():
            kw=self.kwargs.get(n, {})
            if type(s)==dict:
                kw.update(s)
                settings[n]=kw
        self.kwargs.update(settings)

    def setModer(self, moder=Moder):

        c=self.config.get('Moder', {})
        self.moder=moder(
                app=self, config=c)

    def setActions(self):

        def saveSetKeys():

            keys=self.config.get('Keys', {})
            actions=setKeys(self, keys)
            self.actions.update(actions)

        def saveOwnKeys():

            for f in self.__dir__():
                m=getattr(self, f)
                if not f.startswith('__'):
                    self.functions[f]=m
                if hasattr(m, 'modes'):
                    d=(self.name, m.name)
                    if not d in self.actions:
                        self.actions[d]=m 
        saveSetKeys()
        saveOwnKeys()

    def createFolder(
            self, folder=None, fname='folder'):
        
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
            p=f'{self.path}/{f}'
            self.files[f]=p
            if f=='config.toml':
                with open(p, 'rb') as y:
                    tdata=tomli.load(y)
                self.config.update(tdata)

    def setSettings(self):

        s=self.config.get('Settings', {})
        for n, v in s.items():
            setattr(self, n, v)

    def open(self, source=None, **kwargs):

        for r in self.renders:
            if not r.isCompatible(source):
                continue
            return r.open(source, **kwargs)
