from plug.plugs.handler import Handler

class Umay(Handler):

    def __init__(self, 
                 *args, 
                 umay_port=None,
                 **kwargs):

        self.umay_port=umay_port
        super(Umay, self).__init__(
                *args, **kwargs)

    def setup(self):

        super().setup()
        self.setApp()
        self.setConnect(self.umay_port)

    def setApp(self):

        self.app=self.kwargs.get('app', None)
        if self.app:
            self.app.plugman.plugsLoaded.connect(
                    self.load)

    def load(self, plugs):

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
        if intents: 
            paths+=[intents]
        if entities: 
            paths+=[entities]
        return paths

    def getKeyword(self, plug):

        return plug.kwargs.get(
                'keyword', plug.name)

    def handle(self, request):
        raise
