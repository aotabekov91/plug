import os
import json
from pathlib import Path

def createFolder(
        folder, 
        parents=True, 
        exist_ok=True):

        f=os.path.expanduser(folder)
        path=Path(f)
        if not os.path.exists(f): 
            path.mkdir(
                    parents=parents, 
                    exist_ok=exist_ok
                    )
        return path
   
def setKeys(obj, keys):

    actions={}
    for f, k in keys.items():
        m=getattr(obj, f, None)
        if m and hasattr(m, '__func__'):
            func=m.__func__
            fname=func.__name__
            n=getattr(m, 'name', fname)
            setattr(func, 'name', n)
            if type(k)==str: 
                k={'key':k}
            for a, v in k.items():
                setattr(func, a, v)
            actions[(obj.name, m.name)]=m
    return actions

def pretty_json(data, indent=4):

    parsed = json.loads(data)
    return json.dumps(parsed, indent=4)
