import os
import sys
import importlib
from collections.abc import Iterable
from plug.utils.miscel import dotdict

class Moder:

    def __init__(
            self, 
            rtp={},
            app=None,
            config={},
            actions={},
            plugs=dotdict(),
            default='normal',
            **kwargs,
            ):

        self.app=app
        self.rtp=rtp
        self.prev=None
        self.plugs=plugs
        self.current=None
        self.config=config
        self.actions=actions
        self.default=default
        super().__init__(**kwargs)
        self.setup()

    def setup(self):
        self.setSettings()

    def setSettings(self):

        s=self.config.get('Settings', {})
        for n, v in s.items():
            setattr(self, n, v)

    def getState(self):
        return self.current, self.prev

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
            plugs=[], 
            params={},
            **kwargs,
            ):

        def isLoaded(plug_class):
            for p in self.plugs:
                if p.__class__==plug_class:
                    return True
            return False

        if type(plugs)!=set:
            iter=isinstance(plugs, Iterable)
            if not iter: plugs=[plugs]
            plugs=set(plugs)

        plugs=self.getPlugs(plugs)
        for p in plugs: 
            if not isLoaded(p): 
                n=p.__name__
                config=self.app.config.get(
                        n, {})

                # try:

                kwargs=params.get(n, {})
                plug=p(
                      app=self.app, 
                      config=config, 
                      **kwargs
                      )
                self.add(plug)

                # except Exception as e:
                #     print('Error in plug loading: ', n)
                #     print(e)

        self.on_plugsLoaded(self.plugs)

    def add(self, plug):

        name=plug.name.lower()
        self.plugs[name]=plug
        self.save(plug, plug.actions)

    def get(self, m):

        m=m or self.default
        if type(m)==str:
            m=self.plugs.get(m.lower())
        return m

    def set(self, mode=None):

        c=self.current
        m=self.get(mode)
        if m and c!=m:
            if c: c.delisten()
            self.setState(m)
            m.listen()
            return m 

    def setState(self, mode):

        c, _ = self.current, self.prev 
        self.current, self.prev = mode, c

    def save(self, plug, actions): 
        self.actions[plug]=actions

    def on_plugsLoaded(self, plugs): 
        pass
