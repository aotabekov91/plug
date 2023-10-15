import os
from plug import Plug
from functools import partial

class Keyer(Plug):

    def __init__(
            self, 
            *args, 
            **kwargs):

        self.keys={}
        self.modes=[]
        self.default=None
        self.current=None
        super().__init__(
                *args, **kwargs)
        self.current=self.default

    def setup(self):

        super().setup()
        self.setKeys()

    def setKeys(self):

        def assignKeys(keys):

            for n, k in keys.items():
                f=partial(self.actOnKey, n)
                self.functions[n]=f

        self.functions={}
        self.keys=getattr(
                self, 'Keys', {})
        if len(self.modes)==0:
            assignKeys(self.keys)
        else:
            for m in self.modes:
                keys=self.keys.get(m, {})
                assignKeys(keys)

    def actOnKey(
            self, 
            action, 
            digit=1,
            **kwargs,
            ):

        if self.modes:
            c_keys=self.keys.get(
                    self.current, {})
            keys=self.keys.get(
                    self.default, {})
            keys=keys.copy()
            keys.update(c_keys)
        else:
            keys=self.keys
        key=keys.get(action, None)
        if type(key)==dict:
            toggler=kwargs.get(
                    'toggler', None)
            key=key.get(
                    toggler, None)
        if key:
            self.actOnKeyPre(key, action)
            if len(key)==1:
                cmd='xdotool type --clearmodifiers '
                cmd+=f'type {key}'
                for i in range(digit):
                    self.runCommand(cmd) 
            else:
                cmd='xdotool key --clearmodifiers '
                cmd+=f'--repeat {digit} {key}'
                self.runCommand(cmd) 

    def actOnKeyPre(self, key, action):

        if key=='Escape':
            self.actOnEscape()

    def actOnEscape(self):
        self.current=self.default

    def runCommand(self, cmd):
        os.popen(cmd)
