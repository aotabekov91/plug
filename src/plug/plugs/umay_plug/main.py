import io
import yaml
from plug.plugs.handler import Handler

class Umay(Handler):

    def __init__(
            self, 
            *args, 
            wait_time=5, 
            umay_port=None, 
            pollerize=True, 
            adjuster={'digit':int}, 
            **kwargs
            ):

        self.current=None
        self.adjuster=adjuster
        self.umay_port=umay_port
        self.pollerize=pollerize
        self.wait_time=wait_time
        super(Umay, self).__init__(
                *args, **kwargs)
        self.run()

    def setup(self,
              socket_kind='bind'):

        super().setup()
        self.setConnect(
                port=self.port,
                socket_kind=socket_kind,
                )
        self.setUmayConnect()
        self.setApp()

    def setUmayConnect(self):

        self.usocket=self.connect.get('REQ')
        self.usocket.connect(
                f'tcp://localhost:{self.umay_port}')

    def setApp(self):

        if self.app:
            moder=getattr(
                    self.app, 'moder', None)
            if moder:
                if hasattr(moder, 'plugsLoaded'):
                    moder.plugsLoaded.connect(
                        self.register)
                elif hasattr(moder, 'on_plugsLoaded'):
                    moder.on_plugsLoaded=self.register

    def getKeywords(self, obj):

        keywords=getattr(
                obj, 'keywords', [])
        keywords+=obj.kwargs.get(
                'keywords', [])
        keywords.insert(0, obj.name)
        keywords.insert(1, obj.name.lower())
        return keywords

    def register(self, plugs):

        data={
            'kind':'PUSH', 
            'app': self.app.name,
            'port': self.connect.port,
            }
        data['app_keys']=self.getKeywords(
                self.app)
        mode_keys=[] 
        for n, p in plugs.items(): 
            mode_keys+=[self.getKeywords(p)]
        data['mode_keys']=mode_keys
        units={}
        for n, p in plugs.items(): 
            units[n]=self.getUnits(p)
        data['units']=units
        res=self.send({'register': data})
        # print('Umay plug:', res)

    def send(self, data):

        return self.connect.send(
                data=data,
                socket=self.usocket,
                wait_time=self.wait_time,
                pollerize=self.pollerize
                )

    def getUnits(self, plug):

        units=[]
        paths=self.getFiles(plug)
        for path in paths:
            units+=self.readYaml(path)
        for unit in units:
            self.setPlugData(plug, unit)
        return units

    def readYaml(self, path):

        with io.open(path, encoding="utf8") as f:
            yunits = yaml.safe_load_all(f)
            return list(yunits)

    def setPlugData(self, plug, unit):

        kind=unit.get('type', None)
        name=unit.get('name', None)
        if kind=='intent' and name:
            unit['name']='_'.join(
                    [
                     self.app.name, 
                     plug.name, 
                     name
                    ])
        return unit 

    def getFiles(self, plug):

        paths=[]
        umay_yaml=plug.files.get(
                'umay.yaml', None)
        if umay_yaml: 
            paths+=[umay_yaml]
        return paths

    def handle(self, request):

        print('Umay handling request: ', request)
        for name, params in request.items():
            parsed=self.parseName(name)
            if parsed:
                mode, action = parsed 
                plug=self.app.moder.plugs.get(
                        mode.lower(), 
                        self.app.moder.current
                        )
                self.runPlugAction(
                        plug, 
                        action, 
                        params,
                        request,
                        )

    def parseName(self, name):

        l=name.split('_')
        if len(l)==2:
            return l[0], l[1]

    def runPlugAction(
            self, 
            plug, 
            action, 
            params, 
            request
            ):

        if plug:
            f=plug.functions.get(action, None)
            h=getattr(plug, 'handleRequest', None)
            self.adjustParameters(params)
            if f: 
                f(**params)
            elif h:
                h(request)
            else:
                self.checkEars(action, params)

    def adjustParameters(self, prm):

        for n, f in self.adjuster.items():
            if n in prm:
                prm[n]=f(prm[n])

    def checkEars(self, action, prm):

        def checkEar(ear, action):

            if ear and ear.listening:
                func=ear.methods.get(
                        action, None)
                if func:
                    return func 

        def checkParent(cobj, eobj):

            if eobj.parent() is None:
                return False
            elif cobj==eobj:
                return True
            elif eobj.parent()==cobj:
                return True
            return checkParent(
                    cobj, eobj.parent())

        if self.app:
            cear=self.app.qapp.current
            f=checkEar(cear, action)
            if f:
                return f(**prm)
            cand=[]
            for e in self.app.qapp.ears:
                if not e.listening:
                    continue
                v=getattr(e.obj, 'isVisible', None)
                if v and v():
                    f=checkEar(e, action)
                    if f: cand+=[(e, f)]
            if len(cand)==1:
                e, f = cand[0]
                return f(**prm)
            elif len(cand)>1:
                for e, f in cand:
                    if checkParent(cear.obj, e.obj):
                        return f(**prm)
