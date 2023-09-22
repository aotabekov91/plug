import os
import tomli
import inspect
from pathlib import Path
from types import MethodType, BuiltinFunctionType

from plug.utils import Plugman

class Actionable:

    def setActions(self, obj=None):

        if self.config.get('Keys'):
            keys=self.config['Keys']
            for f, key in keys.items():
                m=getattr(self, f, None)
                if m and hasattr(m, '__func__'):
                    if type(key)==str:
                        modes=getattr(m, 'modes', ['command'])
                        setattr(m.__func__, 'key', f'{key}')
                    elif 'key' in key:
                        modes=getattr(m, 'modes', ['command'])
                        modes=key.get('modes', modes)
                        key=key.get('key')
                    f=getattr(m, 'name', m.__func__.__name__)
                    setattr(m.__func__, 'name', f)
                    setattr(m.__func__, 'modes', modes)
                    d=(self.__class__.__name__, m.name)
                    self.actions[d]=m 
                    self.commandKeys[m.key]=m
        if not obj: obj=self
        cnd=[MethodType, BuiltinFunctionType]
        for f in obj.__dir__():
            m=getattr(obj, f)
            if type(m) in cnd and hasattr(m, 'modes'):
                name=getattr(obj, 
                             'name', 
                             obj.__class__.__name__)
                d=(name, m.name)
                if not d in self.actions:
                    self.actions[d]=m 
                    if type(m.key)==str:
                        self.commandKeys[m.key]=m
                    elif type(m.key)==list:
                        for k in m.key: 
                            self.commandKeys[k]=m
