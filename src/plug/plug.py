import os
import tomli
import inspect

from plug.utils import Plugman
from plug.utils.plug_utils import (
        createFolder, 
        setKeys,
        )

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

        def setPlugKeys():

            keys=self.config.get('Keys', {})
            actions=setKeys(self, keys)
            self.actions.update(actions)

        def setPlugOwnKeys():

            for f in self.__dir__():
                m=getattr(self, f)
                if hasattr(m, 'modes'):
                    d=(self.name, m.name)
                    if not d in self.actions:
                        self.actions[d]=m 

        setPlugKeys()
        setPlugOwnKeys()

    def setUIKeys(self, ui=None):

        def setKeys(keys, widget):
            for k, v in keys.items():
                if type(v)==str:
                    pass
            self.setUIKeys(ui)

        ui=getattr(self, 'ui', None)
        keys=self.config.get('Keys', {})
        ui_keys=keys.get('UI', {})
        setKeys(ui_keys, ui)


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
