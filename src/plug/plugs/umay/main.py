import io
import yaml
from plug.plugs.handler import Handler

class Umay(Handler):

    def __init__(self, 
                 *args, 
                 app=None,
                 umay_port=None,
                 **kwargs):

        self.app=app
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
                    self.app, 'plugman', None)
            if plugman:
                plugman.plugsLoaded.connect(
                    self.load)

    def load(self, plugs):

        data={
            'kind':'PUSH', 
            'name': self.name,
            'port': self.connect.port,
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
        for unit in units:
            self.adjustName(plug, unit)
        return units

    def readYaml(self, path):

        with io.open(path, encoding="utf8") as f:
            yunits = yaml.safe_load_all(f)
            return list(yunits)

    def adjustName(self, plug, unit):

        t=unit.get('type', None)
        n=unit.get('name', None)
        if t=='intent' and n:
            pref=[self.name, plug.name, n]
            new_name='_'.join(pref)
            unit['name']=new_name
        return unit
            
    def getFiles(self, plug):

        paths=[]
        umay_yaml=plug.files.get(
                'umay.yaml', None)
        if umay_yaml: 
            paths+=[umay_yaml]
        return paths

    def getKeyword(self, plug):

        return plug.kwargs.get(
                'keyword', plug.name)

    def handle(self, request):

        for k, d in request.items():
            l=k.split('_')
            name, action = l[0], l[1]
            plug=self.app.plugman.plugs.get(
                    name, None)
            if plug:
                func=getattr(plug, action, None)
                if func: func(**d)
