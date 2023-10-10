import os
import time

def command(delay=None, wait=None, kind='os'):

    def _command(func):
        def inner(self, *args, **kwargs):
            if delay: 
                time.sleep(delay)
            cmd = func(self, *args, **kwargs)
            if cmd: 
                if kind=='os': 
                    os.popen(cmd)
            if wait: 
                time.sleep(wait)
        return inner
    return _command
