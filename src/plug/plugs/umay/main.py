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
        self.setConnect(socket_kind='bind')
        self.setUmayConnect()
        self.setApp()

    def setUmayConnect(self):

        self.usocket=self.connect.get('PUSH')
        self.usocket.connect(
                f'tcp://localhost:{self.umay_port}')

    def setApp(self):

        self.app=self.kwargs.get('app', None)
        if self.app:
            self.app.plugman.plugsLoaded.connect(
                    self.load)

    def load(self, plugs):

        plug_data={}
        for n, p in plugs.items(): 
            name=p.__class__.__name__
            plug_data[name]={
                   'kind': 'PUSH', 
                   'port': self.connect.port,
                   'paths': self.getFilePaths(p),
                   'keyword': self.getKeyword(p),
                   }
        data={'data': plug_data}
        self.usocket.send_json(
                {'register': data})
        print(self.umay_port, data)
            
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
