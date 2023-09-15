import os
import sys
import importlib

from .picky import Picky
from .miscel import dotdict

class Plugman:

    def __init__(self, app=None):

        super(Plugman, self).__init__()
        self.app=app
        self.prev=None
        self.current=None
        self.actions={}
        self.all_actions={}
        self.plugs=dotdict()
        self.setup()
        self.picky=Picky(
                self.picky,
                self.folder,
                self.base)

    def installPicks(self): 

        self.picky.install()

    def updatePicks(self): 

        self.picky.update()

    def cleanupPicks(self): 

        self.picky.cleanup()

    def setup(self):

        c=dotdict(self.app.config.get(
            'Plugman', {}))
        self.picky=c.Picky
        self.base=c.Settings.get('base')
        self.folder=os.path.expanduser(
                c.Settings.get('folder'))
        self.app.createFolder(
                self.folder, 'plugman_folder')

    def load(self):

        plugs=[]
        for name, folder in self.picky.rtp.items():
            sys.path.insert(0, folder)

            try:

                m=importlib.import_module(name)
                if hasattr(m, 'get_plug_class'):
                    plugs+=[m.get_plug_class()]

            except ModuleNotFoundError:
                print(f'Module {name} not found')

        self.loadPlugs(plugs)
        self.set('normal')

    def loadPlugs(self, plugs):

        for p in plugs: 
            name=p.__name__
            config=self.app.config.get(name, {})
            plug=p(app=self.app, config=config)
            self.add(plug)

    def add(self, plug):

        self.plugs[plug.name]=plug

    def set(self, listener='normal'):

        if type(listener)==str:
            listener=self.plugs.get(listener)
        if self.current!=listener:
            if self.current: 
                self.current.delisten()
            self.prev=self.current
            self.current=listener
            self.current.listen()

    def register(self, plug, actions): 

        self.actions[plug]=actions
        for n, a in actions.items():
            name='_'.join(n)
            self.all_actions[name]=a
