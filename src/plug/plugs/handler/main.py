from inspect import signature

from plug import Plug
from plug.plugs.connect import Connect

class Handler(Plug):

    def __init__(
            self, 
            *args, 
            port=None, 
            **kwargs):

        self.port=port
        super(Handler, self).__init__(
                *args, **kwargs)

    def setConnect(self, 
                   port=None, 
                   connect=Connect):

        if port:
            self.connect=connect(
                    port=port,
                    handler=self.handle,
                    )
            self.run()

    def run(self):

        self.connect.set()
        self.connect.run()

    def getFunc(self, action, obj=None):

        if obj:
            return getattr(obj, action, None)
        else:
            app=getattr(self, 'app', None)
            if app:
                a=app.plugman.all_actions
                return a.get(action, None)

    def handle(self, r):

        part=r.get('part', None)
        action=r.get('action', None)
        if part:
            obj=self
            parts=part.split('.')
            for p in parts: 
                obj=getattr(obj, p, None)
                if not obj: break
            func=self.getFunc(action, obj)
        else:
            func=self.getFunc(action)
        if func:
            try:
                prm={}
                sig=signature(func)
                for p in sig.parameters:
                    if p in r: 
                        prm[p]=r[p] 
                func(**prm)
            except ValueError:
                func()
