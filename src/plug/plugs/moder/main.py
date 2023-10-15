import os
import sys
import importlib
from plug import Plug
from plug.utils.miscel import dotdict

class Moder(Plug):

    def __init__(
            self, 
            *args,
            rtp={},
            plugs=dotdict(),
            default='normal',
            **kwargs,
            ):

        self.rtp=rtp
        self.prev=None
        self.current=None
        self.plugs=plugs
        self.default=default
        super().__init__(
                *args, **kwargs)
        self.actions={}

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

    def load(
            self, 
            params={},
            plugs=set(), 
            **kwargs,
            ):

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
                kwargs=params.get(
                        p.__name__, {})
                plug=p(app=self.app, 
                       config=config,
                       **kwargs)
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
        if hasattr(plug, 'modeWanted'):
            plug.modeWanted.connect(
                    self.set)
        if hasattr(plug, 'forceDelisten'):
            plug.forceDelisten.connect(
                    self.set)
        if hasattr(plug, 'delistenWanted'):
            plug.delistenWanted.connect(
                    self.set)

    def get(self, mode):

        if mode is None:
            mode=self.default
        if type(mode)==str:
            name=mode.lower()
            mode=self.plugs.get(name)
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

        # for n, a in actions.items():
        #     name='_'.join(n)
        #     self.all_actions[name]=a

    def on_plugsLoaded(self, plugs): 
        pass
