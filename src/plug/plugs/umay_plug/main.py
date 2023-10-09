import io
import yaml
from plug.plugs.handler import Handler

class Umay(Handler):

    def __init__(self, 
                 *args, 
                 umay_port=None,
                 wait_time=5000,
                 pollerize=True,
                 **kwargs):

        self.current=None
        self.umay_port=umay_port
        self.pollerize=pollerize
        self.wait_time=wait_time
        super(Umay, self).__init__(
                *args, **kwargs)
        self.run()

    def setup(self):

        super().setup()
        self.setConnect(
                port=self.port,
                socket_kind='bind'
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
                    self.app, 
                    'moder', 
                    None)
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
        print('Umay plug:', res)

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
        for n, prm in request.items():
            l=n.split('_')
            if len(l)==2:
                m, a = l[0], l[1]
                plugs=self.app.moder.plugs
                p=plugs.get(
                        m, self.app.moder.current)
                p=plugs.get(m.lower(), p)
                if p:
                    f=getattr(p, a, None)
                    h=getattr(p, 'handle', None)
                    if f: 
                        self.adjustParameters(prm)
                        f(**prm)
                    elif h:
                        h(request)
                    else:
                        self.checkEars(a, prm)

    def adjustParameters(self, prm):

        if 'digit' in prm:
            prm['digit']=int(prm['digit'])

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
            uiman=getattr(self.app, 'uiman')
            c=uiman.current
            if uiman.current:
                f=checkEar(c, action)
                if f:
                    return f(**prm)
                cand=[]
                for e in uiman.ears:
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
                        if checkParent(c.obj, e.obj):
                            return f(**prm)
