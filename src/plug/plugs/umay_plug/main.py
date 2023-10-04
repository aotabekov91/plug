import io
import yaml
from plug.plugs.handler import Handler

class Umay(Handler):

    def __init__(self, 
                 *args, 
                 umay_port=None,
                 **kwargs):

        self.current=None
        self.umay_port=umay_port
        super(Umay, self).__init__(
                *args, **kwargs)
        self.run()

    def setName(self):

        super().setName()
        if self.app:
            self.name=self.app.name

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

        if self.app:
            plugman=getattr(
                    self.app, 
                    'plugman', 
                    None)
            if plugman:
                if hasattr(plugman, 'plugsLoaded'):
                    plugman.plugsLoaded.connect(
                        self.load)
                elif hasattr(plugman, 'on_plugsLoaded'):
                    plugman.on_plugsLoaded=self.load

    def getKeywords(self, obj):

        keywords=getattr(
                obj, 'keywords', [])
        if not keywords:
            keywords=obj.kwargs.get(
                    'keywords', [])
        keywords.insert(0, obj.name)
        keywords.insert(1, obj.name.lower())
        return keywords

    def load(self, plugs):

        data={
            'kind':'PUSH', 
            'app': self.name,
            'port': self.connect.port,
            'keywords': self.getKeywords(self.app),
            }

        units={}
        for n, p in plugs.items(): 
            units[n]=self.getUnits(p)
        data['units']=units
        self.usocket.send_json(
                {'register': data})

    def getUnits(self, plug):

        units=[]
        paths=self.getFiles(plug)
        for path in paths:
            units+=self.readYaml(path)
        punits=[]
        for unit in units:
            punits+=[self.setPlugData(
                    plug, unit)]
        return punits

    def readYaml(self, path):

        with io.open(path, encoding="utf8") as f:
            yunits = yaml.safe_load_all(f)
            return list(yunits)

    def setPlugData(self, plug, unit):

        t=unit.get('type', None)
        n=unit.get('name', None)
        if t=='intent' and n:
            pref=[self.name, plug.name, n]
            new_name='_'.join(pref)
            unit['name']=new_name

        return {
                'unit': unit, 
                'keywords': self.getKeywords(plug)
                }
            
    def getFiles(self, plug):

        paths=[]
        umay_yaml=plug.files.get(
                'umay.yaml', None)
        if umay_yaml: 
            paths+=[umay_yaml]
        return paths

    def handle(self, request):

        print('Umay handling request: ', request)
        for n, d in request.items():
            l=n.split('_')
            mode, action = l[0], l[1]
            plug=self.app.plugman.plugs.get(
                    mode, None)
            if not plug:
                plug=self.app.plugman.current
            if plug:
                func=getattr(plug, action, None)
                if func: 
                    func(**d)
                else:
                    handle=getattr(
                            plug, 'handle', None)
                    if handle:
                        handle(request)
