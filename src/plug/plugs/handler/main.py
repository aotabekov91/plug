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
                   connect=Connect,
                   parent_port=None,
                   **kwargs,
                   ):

        self.connect=connect(
                port=port,
                handler=self.handle,
                parent_port=parent_port,
                )
        self.connect.set(**kwargs)

    def stop(self):
        self.running=False
        self.connect.stop()

    def run(self):

        self.running=True
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
        return res
