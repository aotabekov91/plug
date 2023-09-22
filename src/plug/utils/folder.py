import os
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
