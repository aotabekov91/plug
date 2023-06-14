import os
import time
import asyncio

def key(key):
    def _key(func):
        def inner(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        inner.key=key
        return inner
    return _key

def command(finishCheck=False, windowCheck=False, commandType='os', delay=None, wait=None):
    def _command(func):
        def inner(self, request={}, *args, **kwargs):
            cond=True
            if windowCheck:
                if self.window_classes != 'all':
                    cond = self.get_window_class() in self.window_classes
            if delay: time.sleep(delay)
            if cond: 
                cmd = func(self, request, *args, **kwargs)
                if cmd:
                    if hasattr(self, 'parse_repeats'):
                        times = self.parse_repeats(request)
                        cmd = cmd.format(repeat=times)
                    print(f'Running command: {cmd}')
                    if commandType=='i3':
                        asyncio.run(self.manager.command(cmd))
                    elif commandType=='os':
                        os.popen(cmd)
            if wait: time.sleep(wait)
            if finishCheck:
                if hasattr(self, 'checkAction'):
                    self.checkAction(request)
                elif hasattr(self, 'mode'):
                    self.mode.checkAction(request)
        return inner
    return _command
