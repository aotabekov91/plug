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

        self.usocket=self.connect.get('REQ')
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
        keywords+=obj.kwargs.get(
                'keywords', [])
        keywords.insert(0, obj.name)
        keywords.insert(1, obj.name.lower())
        return keywords

    def load(self, plugs):

        data={
            'kind':'PUSH', 
            'app': self.name,
            'port': self.connect.port }
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
        res=self.connect.send(
                {'register': data},
                self.usocket)
        print(res)

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

    def handle(self, request):

        # print('Umay handling request: ', request)
        for n, prm in request.items():
            l=n.split('_')
            if len(l)==2:
                m, a = l[0], l[1]
                plug=self.app.plugman.plugs.get(
                        m, self.app.plugman.current)
                if plug:
                    f=getattr(plug, a, None)
                    h=getattr(plug, 'handle', None)
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
