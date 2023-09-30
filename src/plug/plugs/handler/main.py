from inspect import signature

from plug import Plug
from plug.plugs.connect import Connect

class Handler(Plug):

    def __init__(
            self, 
            *args, 
            port=None, 
            respond=False,
            **kwargs):

        self.port=port
        self.respond=respond

        super(Handler, self).__init__(
                *args, **kwargs)

    def setConnect(self, 
                   port=None, 
                   parent_port=None,
                   connect=Connect,
                   **kwargs,
                   ):

        self.connect=connect(
                port=port,
                handler=self.handle,
                parent_port=parent_port,
                )
        self.connect.set(**kwargs)

    def run(self):

        self.connect.run()

    def getFunc(self, action, obj=None):

        if action.startswith('app.'):
            app=getattr(self, 'app', None)
            if app:
                parts=action.split('.')
                obj=app
                for p in parts: 
                    obj=getattr(obj, p, None)
                return obj 
        elif obj:
            return getattr(obj, action, None)
        else:
            return getattr(self, action, None)

    def runFunc(self, name, args):

        func=self.getFunc(name)
        if func: 
            return func(**args)

    def handle(self, req):

        print(f'{self.name} received request: {req}')

        res={}
        for name, args in req.items():
            res[name]=self.runFunc(name, args)

        if self.respond: 
            return res
