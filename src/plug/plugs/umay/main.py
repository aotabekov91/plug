from plug import Plug
from plug.plugs.connect import Connect

class Umay(Plug):

    def __init__(self, 
                 *args, 
                 app=None,
                 umay_port=19999,
                 **kwargs):

        self.app=app
        self.umay_port=umay_port
        self.connect=Connect(app)
        super().__init__(*args, **kwargs)
        self.app.plugman.plugsLoaded.connect(
                self.on_plugsLoaded)

    def setup(self):

        umay_port=self.app.config.get(
                'umay_port', None)
        if umay_port:
            self.umay_port=umay_port
        self.setConnection()

    def setConnection(self, connect=Connect):

        self.connect=connect(
                self.app,
                handler=self.handle,
                parent_port=self.umay_port,
                )
        self.connect.set()

    def on_plugsLoaded(self, plugs):

        data=[]
        for n, p in plugs.items(): 
            paths = self.getFilePaths(p)
            if not paths: continue
            pdata={'kind': 'PUSH', 
                   'action': 'register',
                   'port': self.connect.port,
                   'mode': p.__class__.__name__,
                   'keyword': self.getKeyword(p),
                   'paths': self.getFilePaths(p)
                   }
            data+=[pdata]
        self.connect.send(data)
        self.connect.run()
            
    def getFilePaths(self, plug):

        paths=[]
        intents=plug.files.get(
                'intents.yaml', None)
        entities=plug.files.get(
                'entities.yaml', None)
        if intents: paths+=[intents]
        if entities: paths+=[entities]
        return paths

    def getKeyword(self, plug):

        return plug.kwargs.get(
                'keyword', plug.name)

    def handle(self, request):
        raise
