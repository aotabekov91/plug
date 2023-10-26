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

    def connect(self):

        w=getattr(self.app, 'window')
        if w:
            w.focusGained.connect(
                self.on_focused)

    def on_focused(self):
        self.set(self.current)

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
                n=p.__name__
                c=self.app.config.get(n, {})

                # try:

                kwargs=params.get(n, {})
                plug=p(app=self.app, 
                       config=c, 
                       **kwargs)
                self.add(plug)

                # except Exception as e:
                #     print('Error in plug loading: ', n)
                #     print(e)

        self.on_plugsLoaded(self.plugs)
        self.connect()
        self.set()

    def add(self, plug):

        name=plug.name.lower()
        self.plugs[name]=plug
        self.save(plug, plug.actions)
        if hasattr(plug, 'modeWanted'):
            plug.modeWanted.connect(
                    self.set)
        # if hasattr(plug, 'focusGained'):
            # plug.focusGained.connect(
                    # self.on_focusGained)
        # if hasattr(plug, 'forceDelisten'):
            # plug.forceDelisten.connect(
                    # self.set)
        if hasattr(plug, 'delistenWanted'):
            plug.delistenWanted.connect(
                    self.set)

    # def on_focusGained(self, mode=None):
    #     if self.current!=mode:
    #         if not self.current:
    #             self.set(mode)
    #         elif self.current.follow_focus:
    #             self.set(mode)

    def get(self, mode):

        if mode is None:
            mode=self.default
        if type(mode)==str:
            name=mode.lower()
            mode=self.plugs.get(name)
        return mode

    def set(self, mode=None):

        m=self.get(mode)
        p=self.current
        if m:# and current!=mode:
            if p: p.delisten()
            self.current, self.prev=m, p
            self.current.listen()

    def save(self, plug, actions): 
        self.actions[plug]=actions

    def on_plugsLoaded(self, plugs): 
        pass
