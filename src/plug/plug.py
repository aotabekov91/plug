import os
import tomli
from plug import utils
from inspect import getfile

class Plug:

    name=None
    isMode=False
    isMainApp=False

    def __init__(
            self, 
            app=None,
            config={},
            **kwargs):

        super().__init__()
        self.app=app
        self.files={}
        self.actions={}
        self.functions={}
        self.config=config
        self.kwargs=kwargs
        self.setup()

    def setName(self):

        if self.name is None: 
            c=self.__class__
            self.name=c.__name__

    def setup(self):

        self.setName()
        self.setBasePath()
        self.setFiles()
        self.setSettings()
        self.updateArgs()
        self.setActions()
        if self.isMainApp:
            self.app=self
            self.setModer()
            self.setHandler()

    def setHandler(
            self, 
            handler=utils.Handler):

        c=self.config.get('Handler', {})
        self.handler=handler(
                app=self, config=c)

    def open(self, *args, **kwargs):

        return self.handler.handleOpen(
                *args, **kwargs)

    def setModer(self, moder=utils.Moder):

        c=self.config.get('Moder', {})
        self.moder=moder(
                app=self, config=c)

    def updateArgs(self):

        settings=self.config.get(
                'Settings', {})
        for n, s in settings.items():
            kw=self.kwargs.get(n, {})
            if type(s)==dict:
                kw.update(s)
                settings[n]=kw
        self.kwargs.update(settings)

    def setActions(self):

        def saveSetKeys():

            keys=self.config.get('Keys', {})
            actions=utils.setKeys(self, keys)
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
        p=utils.createFolder(folder)
        setattr(self, fname, p)

    def setBasePath(self):

        f=getfile(self.__class__)
        a=os.path.abspath(f)
        p=os.path.dirname(a)
        self.path=p.replace('\\', '/')

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

    def checkProp(self, prop, obj=None):

        ob=obj or self
        if type(prop)!=list: prop=[prop]
        for p in prop:
            c=getattr(ob, p, None)
            if c is None: return False
            if c is False: return False
        return True
