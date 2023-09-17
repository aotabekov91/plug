import re
from plug import Plug

class Systemcut(Plug):

    def __init__(self,
                 *args, 
                 app=None,
                 **kwargs):

        self.app=app
        super().__init__(*args, **kwargs)

    def setup(self):

        super().setup()
        self.setSystemShortcut()

    def setSystemListener(self): pass

    def setSystemShortcut(self):

        if self.app.config.get('System'):
            self.setSystemListener()
            shortcuts=self.config['System']
            for func_name, key in shortcuts.items():
                func=getattr(self, func_name, None)
                key=re.sub(r'(Shift|Alt|Ctrl)', 
                           r'<\1>', 
                           key).lower() 
                if func: 
                    self.os_listener.listen(key, func)
