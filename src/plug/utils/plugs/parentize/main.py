import inspect
from plug import Plug
from plug.plugs.connect import Connect

class Parentize(Plug):

    def __init__(self, 
                 *args, 
                 app=None,
                 port=None,
                 parent_port=None,
                 **kwargs):

        self.app=app
        self.port=port
        self.parent_port=parent_port
        super().__init__(*args, **kwargs)

    def setup(self):

        super().setup()
        self.parent_port=getattr(
                self.app, 'parent_port', None)
        self.setConnection()

    def setConnection(self):

        self.connect=Connect(
            app=self.app,
            handler=self.handle,
            parent_port=self.parent_port,
        )
        self.connect.set()
        data={'command': 'register', 
              'mode': self.__class__.__name__, 
              'port': self.connect.port, 
              'kind': 'PUSH'}
        self.connect.send([data])
        self.connect.run()

    def handle(self, r):

        a=r.get('action', {})
        f=getattr(self, a, None)
        if f:
            prm=inspect.signature(f).parameters
            fp={}
            for p in prm:
                if p in r: fp[p]=r[p] 
            f(**fp)
