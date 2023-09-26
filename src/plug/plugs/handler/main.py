import inspect

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

    def setup(self):

        super().setup()
        self.setConnect(self.port)
        
    def setConnect(
            self, port, connect=Connect):

        if port:
            self.connect=connect(
                    port=port,
                    handler=self.handle,
                    )
            self.run()

    def run(self):

        self.connect.set()
        self.connect.run()

    def handle(self, request):

        part=request.get('part', None)
        action=request.get('action', None)
        if part:
            obj=self
            parts=part.split('.')
            for p in parts: 
                obj=getattr(obj, p, None)
                if not obj: break
            func=getattr(obj, action, None)
        else:
            func=self.app.plugman.all_actions.get(
                    action, None)
        if func:
            try:
                prm=inspect.signature(func).parameters
                fp={}
                for p in prm:
                    if p in request: fp[p]=request[p] 
                func(**fp)
            except ValueError:
                func()
