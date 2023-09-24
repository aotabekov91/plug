import os
import sys
import importlib

from .picky import Picky
from .miscel import dotdict

class Plugman:

    def __init__(self, app=None):

        self.install_requirements=True
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
        if self.install_requirements:
            self.installRequirements()

    def installRequirements(self):

        self.picky.installRequirements()

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

    def getPicks(self):

        plugs=[]
        for n, f in self.picky.rtp.items():
            if os.path.exists(f):
                sys.path.insert(0, f)
                try:
                    m=importlib.import_module(n)
                    k=getattr(m, 'get_plug_class', None)
                    if k: plugs+=[k()]
                except Exception as e:
                    msg='Error in plug importing: '
                    print(msg, n)
                    print(e)
        return plugs

    def loadPicks(self):

        plugs=self.getPicks()
        self.loadPlugs(plugs)
        normal=self.plugs.get('normal')
        if normal:
            self.set(normal)
        else:
            self.installPicks()
            if not self.install_requirements:
                self.installRequirements()
            plugs=self.getPicks()
            self.loadPlugs(plugs)
            self.set('normal')

    def loadPlugs(self, plugs, force=False):

        def isLoaded(plug_class):

            for p in self.plugs:
                if p.__class__==plug_class:
                    return True
            return False

        for p in plugs: 

            if isLoaded(p) and not force: 
                continue

            n=p.__name__
            c=self.app.config.get(n, {})
            try:
                plug=p(app=self.app, config=c)
                self.add(plug)
            except Exception as e:
                print('Error in plug loading: ', n)
                print(e)

    def add(self, plug):

        self.plugs[plug.name]=plug

    def set(self, mode='normal'):

        if type(mode)==str:
            mode=self.plugs.get(mode)
        if self.current!=mode:
            if self.current: 
                self.current.delisten()
            self.prev=self.current
            self.current=mode
            if self.current:
                self.current.listen()

    def saveActions(self, plug, actions): 

        self.actions[plug]=actions
        for n, a in actions.items():
            name='_'.join(n)
            self.all_actions[name]=a
