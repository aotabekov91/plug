import inspect

from plug import Plug
from plug.plugs.connect import Connect

class Handler(Plug):

    def __init__(self, 
                 *args,
                 app=None,
                 port=None,
                 **kwargs): 

        self.app=app
        self.port=port
        super().__init__(*args, **kwargs)

    def setup(self):

        super().setup()
        port=getattr(self.app, 'handler_port')
        if port: self.port=port
        self.setConnection()

    def setConnection(self, connect=Connect):

        self.connect=connect(
                self.app,
                port=self.port,
                handler=self.handle,
                )
        self.connect.set()
        self.connect.run()

    # def getActions(self):
    #     data={}
    #     actions=self.app.plugman
    #     for plug, actions in actions.items():
    #         plug_data=[]
    #         if hasattr(plug, 'name'):
    #             name=plug.name
    #         else:
    #             name=plug.__class__.__name__
    #         for d, a in actions.items():
    #             plug_data+=['_'.join(d)]
    #         data[name]=plug_data
    #     return data

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
