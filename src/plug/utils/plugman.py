import os
import sys
import importlib

from picky import Picky

class dotdict(dict):

    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Plugman:

    def __init__(self, app=None, path=None):

        super(Plugman, self).__init__()

        self.app=app
        self.current=None
        
        self.actions={}
        self.all_actions={}
        self.plugs=dotdict()
        self.modes=dotdict()

        self.setup()

        self.picky=Picky(
                self.picky,
                self.folder,
                self.base)

        self.picky.install()

    def setup(self):

        c=dotdict(self.app.config.get('Plugman', {}))

        self.picky=c.Picky
        self.base=c.Settings.get('base')
        self.folder=os.path.expanduser(c.Settings.get('folder'))
        self.app.createFolder(self.folder, 'plugman_folder')

    def load(self):

        plugs=[]
        modes=[]

        for name, folder in self.picky.rtp.items():

            sys.path.append(folder)
        
            m=importlib.import_module(name)
            if hasattr(m, 'get_plug_class'):
                plugs+=[m.get_plug_class()]
            elif hasattr(m, 'get_mode_class'):
                modes+=[m.get_mode_class()]

        self.loadPlugs(plugs)
        self.loadModes(modes)

        self.set('normal')

    def getModes(self): return self.modes

    def loadPlugs(self, plugs):

        for p in plugs: self.add(p(app=self.app), 'plug')

    def loadModes(self, modes):

        for m in modes: self.add(m(app=self.app), 'mode')

    def add(self, picked, kind):

        if kind=='mode':
            self.modes[picked.name]=picked
        elif kind=='plug':
            self.plugs[picked.name]=picked

        if hasattr(picked, 'setPlugData'):
            picked.setPlugData()

    def set(self, listener='normal', kind='mode'):

        if type(listener)==str:
            if kind=='mode':
                listener=self.modes.get(listener, 'normal')
            elif kind=='plug':
                listener=self.plugs.get(listener)

        if self.current!=listener:

            if self.current: 
                self.current.delisten()

            self.current=listener
            self.current.listen()

    def register(self, plug, actions): 

        self.actions[plug]=actions
        for n, a in actions.items():
            name='_'.join(n)
            self.all_actions[name]=a
