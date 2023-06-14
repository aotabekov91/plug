import os
import time
import asyncio

def command(finishCheck=False, windowCheck=False, commandType='os', delay=None, wait=None):
    def _command(func):
        def inner(self, *args, **kwargs):
            cond=True
            if windowCheck:
                if self.window_classes != 'all':
                    cond = self.get_window_class() in self.window_classes
            if delay: time.sleep(delay)
            if cond: 
                cmd = func(self, *args, **kwargs)
                if cmd:
                    print(f'Running command: {cmd}')
                    if commandType=='i3':
                        asyncio.run(self.manager.command(cmd))
                    elif commandType=='os':
                        os.popen(cmd)
            if wait: time.sleep(wait)
            if finishCheck:
                if hasattr(self, 'checkAction'):
                    self.check()
                elif hasattr(self, 'mode'):
                    self.mode.check()
        return inner
    return _command
