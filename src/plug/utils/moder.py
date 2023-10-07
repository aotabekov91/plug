import os
import sys
import importlib
from plug.utils.picky import Picky
from plug.utils.miscel import dotdict

class Moder:

    def __init__(
            self, 
            app=None, 
            config={},
            plugs=dotdict(),
            default='normal',
            ):

        self.rtp={}
        self.app=app
        self.prev=None
        self.actions={}
        self.plugs=plugs
        self.current=None
        self.config=config
        self.all_actions={}
        self.default=default
        super().__init__()
        self.setup()

    def setup(self):

        self.config=dotdict(
                self.app.config.get(
                    'Moder', {}))
        self.setSettings()
        self.setPicky()

    def setPicky(self, picky_class=None):

        if not picky_class:
            picky_class=Picky
        self.picky=picky_class(
                self.app, self)

    def setSettings(self):

        s=self.config.get('Settings', {})
        for k, v in s.items():
            setattr(self, k, v)

    def getPlugs(self, plugs=set()):

        for n, f in self.rtp.items():
            if os.path.exists(f):
                sys.path.insert(0, f)
                try:
                    m=importlib.import_module(n, f)
                    k=getattr(m, 'get_plug_class', None)
                    if k: 
                        plugs.add(k())
                except Exception as e:
                    msg='Error in plug importing: '
                    print(msg, n)
                    print(e)
        return plugs

    def load(self, plugs=set()):

        def isLoaded(plug_class):
            for p in self.plugs:
                if p.__class__==plug_class:
                    return True
            return False

        plugs=self.getPlugs(plugs)
        for p in plugs: 
            if not isLoaded(p): 
                config=self.app.config.get(
                        p.__name__, {})
                # try:
                plug=p(app=self.app, 
                       config=config)
                self.add(plug)
                # except Exception as e:
                #     print('Error in plug loading: ', n)
                #     print(e)
        self.on_plugsLoaded(self.plugs)
        self.set()

    def add(self, plug):

        name=plug.name.lower()
        self.plugs[name]=plug
        self.save(plug, plug.actions)

    def get(self, mode):

        if type(mode)==str:
            mode=self.plugs.get(mode)
        return mode

    def set(self, mode=None):

        if not mode:
            mode=self.default
        mode=self.get(mode)
        if self.current!=mode:
            if self.current: 
                self.current.delisten()
            self.prev=self.current
            self.current=mode
            if self.current:
                self.current.listen()

    def save(self, plug, actions): 

        self.actions[plug]=actions
        for n, a in actions.items():
            name='_'.join(n)
            self.all_actions[name]=a

    def on_plugsLoaded(self, plugs): 
        pass
