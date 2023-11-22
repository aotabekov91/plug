import re
from PyQt5 import QtCore 
from inspect import signature
from PyQt5.QtWidgets import QWidget, QTextEdit, QLineEdit

# (mode, view) -> keys

class EarMan(QtCore.QObject):

    wait_run=5
    wait_time=200
    mode_on_exit='normal'
    delisten_on_exec=False
    delisten_key=[QtCore.Qt.Key_Escape]
    delisten_key_=['<escape>', '<c-['] # Todo
    plugsLoaded=QtCore.pyqtSignal(object)
    keysChanged=QtCore.pyqtSignal(object)
    matchIsExecuted=QtCore.pyqtSignal()
    matchIsToBeExecuted=QtCore.pyqtSignal()

    mapping={
            '@': 'At',
            '+': 'Plus',
            ' ': 'Space',
            '/': 'Slash',
            '-': 'Minus',
            ',': 'Comma', 
            '.': 'Period',
            '$': 'Dollar',
            '*': 'Asterisk',
            ';': 'Semicolon', 
            '_': 'Underscore',
            '[': 'BracketLeft',
            ']': 'BracketRight',
            }

    def __init__(self, app):

        self.app=app
        self.keys={}
        self.ptext=''
        self.pkeys=[]
        self.names={}
        self.obj=None
        self.kwargs={}
        self.all_keys={}
        self.key_leaders={}
        self.listen_leaders={}
        self.commands={}
        super().__init__(app)
        self.app.moder.plugsLoaded.connect(
                self.setPlugs)
        self.app.qapp.installEventFilter(
                self)
        self.setKeyMap()
        self.setTimer()
        
    def setPlugs(self, plugs):

        self.createHolders(plugs)
        self.setPlugLeaders(plugs)
        self.setPlugActions(plugs)
        self.plugsLoaded.emit(plugs)

    def setTimer(self):

        self.timer=QtCore.QTimer()
        f=lambda: self.executeMatch([], [], 0)
        self.timer.timeout.connect(f)
        self.timer.setSingleShot(True)

    def listen(self, obj):

        self.obj=obj
        self.clearKeys()

    def delisten(self, obj):

        self.obj=None
        self.clearKeys()

    def isListening(self, obj):
        return self.obj==obj

    def setPlugLeaders(self, plugs):

        for p in plugs.values():
            l=getattr(p, 'listen_leader', None)
            if l:
                k=self.parseKey(l)
                self.listen_leaders[k]=p
            l=getattr(p, 'leader_keys', None)
            if l:
                for n, k in l.items():
                    nn=n.split('|')
                    d=(p.name, n, None)
                    if len(nn)==2:
                        d=(p.name, nn[0], nn[1])
                    self.key_leaders[d]=k

    def setPlugActions(self, plugs):

        def getModes(m, s):

            if len(m)==0:
                yield (s, s)
                yield (s, None)
                for n in self.names.keys():
                    yield (n, s)
            else:
                for i in m:
                    j=i.split('|')
                    if len(j)==1:
                        yield (i, i)
                        yield (i, None)
                        for n in self.names.keys():
                            yield (n, i)
                    else:
                        for r in j[1].split(':'):
                            yield (j[0], r)

        d={}

        for s in self.app.uiman.m_widgets:
            for f in s.__dir__():
                m=getattr(s, f)
                if hasattr(m, 'modes'):
                    name=s.__class__.__name__
                    if hasattr(s, 'name'):
                        name=s.name()
                    for j in getModes(m.modes, name):
                        if not j in d: d[j]={}
                        t=[name]+list(j)
                        t=tuple(t)
                        pref=self.key_leaders.get(t, '')
                        k=self.parseKey(m.key, pref)
                        for i in k: d[j][i]=(s, m)

        for v in self.app.handlers:
            s=v.view_class()
            if not v: continue
            for f in dir(s):
                m=getattr(s, f)
                if hasattr(m, 'modes') and hasattr(m, 'key'):
                    name=s.__class__.__name__
                    if hasattr(s, 'name'):
                        name=s.name()
                    for j in getModes(m.modes, name):
                        if not j in d: d[j]={}
                        t=[name]+list(j)
                        t=tuple(t)
                        pref=self.key_leaders.get(t, '')
                        k=self.parseKey(m.key, pref)
                        for i in k: d[j][i]=(s, m)

        acs=self.app.moder.actions
        for p, c in acs.items():
            for n, a in c.items():
                for j in getModes(a.modes, p.name):
                    if not j in d: d[j]={}
                    t=[p.name]+list(j)
                    t=tuple(t)
                    pref=self.key_leaders.get(t, '')
                    k=self.parseKey(a.key, pref)
                    for i in k:
                        d[j][i]=(p, a)

        self.all_keys=d

        for n, p in plugs.items():
            self.setActions(p)
            self.setupUIActions(p)

    # def setPlugActions(self, plugs):
    #     for n, p in plugs.items():
    #         self.setActions(p)
    #         self.setupUIActions(p)

    def setupUIActions(self, p):

        k=self.keys[p]
        c=self.commands[p]

        def getAncestorActions(w):

            p=w.parent()
            f=any([p==ui, p in k, p in c])
            if f or p is None:
                key=k.get(p, {})
                command=c.get(p, {})
                return key, command
            return getAncestorActions(p)

        def setWidgetActions(w, upcursive=False):

            key, command={}, {}
            if upcursive:
                key, command=getAncestorActions(w)

            for f in w.__dir__():
                a=getattr(w, f)
                if not hasattr(a, 'tagged'):
                    continue
                if len(a.modes)==0:
                    if a.key:
                        wk=self.parseKey(a.key)
                        key[wk]=a
                    command[a.name]=a
                else:
                    for m in a.modes:
                        t=self.parseMode(m)
                        if not t: continue
                        tt, ts=t[0], t[1]
                        plug=self.names[tt]
                        pkeys=self.keys[plug]
                        pcoms=self.commands[plug]
                        for j in ts:
                            if not j in pkeys: pkeys[j]={}
                            if not j in pcoms: pcoms[j]={}
                            pcoms[j][a.name]=a
                            if a.key:
                                wk=self.parseKey(a.key)
                                pkeys[j][wk]=a

            if key: k[w]=key
            if command: c[w]=command

        ui=getattr(p, 'ui', None)
        if ui:
            setWidgetActions(ui)
            ch=ui.findChildren(QWidget)
            for i in ch: 
                setWidgetActions(i, upcursive=True)

    def createHolders(self, plugs):

        for n, p in plugs.items():
            if p.name in self.commands:
                continue
            self.names[p.name]=p
            self.keys[p]={'default': {}}
            self.commands[p]={'default': {}}

    def setActions(self, obj):

        def check(modes, o, obj):

            for i in modes:
                t=i.split('|', 1)
                if len(t)<2: continue
                m, a = t[0], t[1] 
                if obj.name!=m: continue
                ps=a.split(':')
                d=[]
                for p in ps:
                    d+=[(p, (obj.name, p))]
                return d

        def checkMode(m, o, obj):

            if 'any' in m:
                return [('default', (obj.name,))]
            elif obj.name in m:
                return [('defaut', (obj.name,))]
            elif o==obj and len(m)==0:
                return [('default', (obj.name,))]
            return check(m, o, obj)

        def getPrefix(obj, s, ls):

            n=obj.name
            if s!='default': n=f'{n}|{s}'
            return ls.get(n, '') 

        k=self.keys[obj]
        c=self.commands[obj]
        acs=self.app.moder.actions
        for o, a in acs.items():
            for (pn, n), m in a.items():
                modes=getattr(m, 'modes', [])
                ss=checkMode(modes, o, obj)
                if not ss: continue
                kl=getattr(m, 'key', [])
                # ls=getattr(o, 'leader_keys', {})
                for s, d in ss:
                    if not s in k: k[s]={}
                    if not s in c: c[s]={}

                    pref=self.key_leaders.get(o.name, {})
                    pr=pref.get(d, '')
                    # if pr: print(obj, s, f'{pr}{kl}')
                    # pr=getPrefix(obj, s, ls)
                    # key=self.setKey(obj, o, m, n)
                    key=self.parseKey(kl, pr)
                    if key: k[s][key]=m
                    c[s][n]=m


    # def setKey(self, obj, o, m, n):
        # k=getattr(m, 'key', [])
        # if not k: return
        # l=getattr(o, 'leader_keys', {})
        # p=l.get(obj.name, '')
        # return self.parseKey(k, prefix=p)

    def parseKey(self, key, prefix=''):

        def parseLetter(t, title=True):

            u=[]
            if t.isupper(): 
                u+=[getattr(QtCore.Qt,'ShiftModifier')]
            if title: t=t.upper()
            k=self.mapping.get(t, t)
            u+=[getattr(QtCore.Qt, f"Key_{k}")]
            return u

        def parse(key):

            parsed=[]
            # p=r'(?P<group>(<[acAC]-.>)*)(?P<tail>([^<]*))'
            t=r'(?P<tail>([^<]*))'
            s=r'(?P<special>(<[^>]*>)*)'
            g=r'(?P<group>(<[acAC]-.>)*)'
            p=f'{g}{s}{t}'
            match=re.match(p, key)
            groups=match.group('group')
            if groups:
                groups=re.findall('<([^>]*)>', groups)
                for g in groups:
                    unit=[]
                    t=g.split('-', 1)
                    m, l = t[0], t[1]
                    if m in 'cC':
                        cm=getattr(QtCore.Qt,'ControlModifier')
                        unit+=[cm]
                    elif m in 'aA':
                        am=getattr(QtCore.Qt,'AltModifier')
                        unit+=[am]
                    unit+=parseLetter(l)
                    parsed+=[tuple(unit)]
            special=match.group('special')
            if special:
                special=re.findall('<([^>]*)>', special)
                for s in special:
                    s=s.strip('<').strip('>').title()
                    unit=parseLetter(s, False)
                    parsed+=[tuple(unit)]
            tails=match.group('tail')
            if tails:
                for t in list(tails):
                    unit=parseLetter(t)
                    parsed+=[tuple(unit)]
            return tuple(parsed) 

        p=[]
        if not key: return () 
        if type(key)==str: 
            key=[key]
        for k in key: 
            p+=[parse(f"{prefix}{k}")]
        return tuple(p)

    def eventFilter(self, w, e):

        if not self.obj:
            return False
        if e.type()!=QtCore.QEvent.KeyPress:
            return False
        self.registerKey(e)
        if self.checkLeader(e):
            e.accept()
            return True
        if self.addKeys(e):
            e.accept()
            return True
        elif hasattr(self.obj, 'event_functor'):
            r=self.obj.event_functor(e, self)
            if r:
                e.accept()
                return True
            self.clearKeys()
            return False
        else:
            self.clearKeys()
            return False

    def registerKey(self, e):

        self.pressed=self.getPressed(e)
        if self.pressed and e.text():
            t=self.getText(self.pressed)
            self.ptext+=t
            self.pkeys.append(self.pressed)
            self.keysChanged.emit(self.ptext)

    def getPressed(self, e):

        p = []
        mdf=e.modifiers()
        if (mdf & QtCore.Qt.AltModifier):
            p+=[QtCore.Qt.AltModifier]
        if (mdf & QtCore.Qt.ControlModifier):
            p+=[QtCore.Qt.ControlModifier]
        if (mdf & QtCore.Qt.ShiftModifier):
            if e.text().isalpha():
                p+=[QtCore.Qt.ShiftModifier]
            elif QtCore.Qt.ControlModifier in p:
                p+=[QtCore.Qt.ShiftModifier]
        p+=[e.key()]
        return tuple(p)

    def clearKeys(self):

        self.timer.stop()
        self.ptext=''
        self.pkeys=[]
        self.pressed=None
        self.keysChanged.emit('')

    def checkLeader(self, e):

        for l, p in self.listen_leaders.items():
            if (self.pressed,) in l:
                f=getattr(p, 'checkLeader', None)
                if f:
                    c=f(e, self.pressed)
                    if not c: return False
                self.timer.stop()
                self.timer.timeout.disconnect()
                self.timer.timeout.connect(p.toggle)
                self.timer.start(self.wait_run)
                return True
        return False

    def addKeys(self, e):

        self.timer.stop()
        if e.key() in self.delisten_key:
            self.clearKeys()
            self.obj.deactivate()
            return True
        elif self.pressed:
            m, p = [], []
            k, d = self.getKeys()
            m, p=self.getMatches(k, d, e)
            self.runMatches(m, p, k, d)
            return m or p

    def getKeys(self):

        key, digit = [], ''
        for i, k in enumerate(self.pkeys):
            p=self.key_map[k[0]]
            if p.isnumeric():
                digit+=p
            else:
                key=self.pkeys[i:]
                break
        if digit: 
            digit=int(digit)
        else:
            digit=None
        return tuple(key), digit

    def getMatches(self, k, d, e):

        # def getWKeys(w):

        #     if w==self.obj.ui or w in keys:
        #         return keys.get(w, {})
        #     return getWKeys(w.parent())

        # def getWidgetKeys():

        #     l={}
        #     ui=getattr(self.obj, 'ui', None)
        #     if ui:
        #         w=self.app.qapp.focusWidget()
        #         edits=[QTextEdit, QLineEdit]
        #         mdfs=e.modifiers()
        #         c1=not type(w) in edits
        #         c2=mdfs & QtCore.Qt.ControlModifier
        #         if c1 or c2: 
        #             ch=ui.findChildren(QWidget)
        #             ch.append(ui)
        #             if w in ch: 
        #                 l.update(getWKeys(w))
        #     return l

        # def getTypeKeys(k):

        #     l={}
        #     t=self.app.moder.type()
        #     v=self.app.moder.view()
        #     for s in [v, t]:
        #         sclass=s.__class__
        #         for c in sclass.__mro__[::-1]:
        #             n=c.__name__
        #             if n in k:
        #                 l.update(k.get(n))
        #     r=None
        #     if v: r=v.render()
        #     if r and r.name in k:
        #         l.update(k.get(r.name))
        #     return l

        # m, p, l, i = [], [], [], {}
        # keys=self.keys.get(self.obj, {})
        # wkeys=getWidgetKeys()
        # skeys=getTypeKeys(keys)
        # dkeys=keys.get('default', {})

        mm=self.app.moder.mode()
        vv=self.app.moder.view()
        dd=(mm.name, vv.name())

        # search and update

        # k = {}
        # k = (mode, None, None)
        # k = (mode, view, None)
        # k = (mode, view, type)
        # k = (any, None, None)


        sdd={}
        for i in [vv.name(), 'any', None][::-1]:
            dd=(mm.name, i)
            pp=self.all_keys.get(dd, {})
            sdd.update(pp)

        m, p = [], []
        for c, (o, d) in sdd.items():
            print(c, k)
            if k!=c[:len(k)]: continue
            # if not d is None:
            #     t=getattr(d, '__wrapped__', d)
            #     c1='digit' in signature(t).parameters
            #     if not c1: continue
            if k==c: 
                m+=[d]
            elif k==c[:len(k)]: 
                p+=[d]
        return m, p

        # if wkeys: l.append(wkeys)
        # if dkeys: l.append(dkeys)
        # if skeys: l.append(skeys)
        # for v in l: i.update(v)
        # for v, f in i.items():
        #     for c in v:
        #         if k!=c[:len(k)]: continue
        #         if not d is None:
        #             t=getattr(f, '__wrapped__', f)
        #             c1='digit' in signature(t).parameters
        #             if not c1: continue
        #         if k==c: 
        #             m+=[f]
        #         elif k==c[:len(k)]: 
        #             p+=[f]
        # return m, p

    def runMatches(
            self, 
            matches, 
            partial, 
            key, 
            digit
            ):

        self.timer.timeout.disconnect()
        self.timer.timeout.connect(
                lambda: self.executeMatch(
                    matches, partial, digit))
        if len(matches)==1 and not partial:
            self.timer.start(self.wait_run)
        else:
            if self.wait_time: 
                self.timer.start(self.wait_time)

    def getText(self, pressed):

        p=[]
        shift=False
        for i in pressed:
            n=self.key_map[i]
            if n == 'ControlModifier':
                p+=['c']
            elif n == 'ShiftModifier':
                shift=True
            else:
                if shift: n=n.upper()
                p+=[n]
        if len(p)==1:
            return p[0]
        return f'<{"-".join(p)}>'

    def setKeyMap(self):

        self.key_map={}
        for n, v in vars(QtCore.Qt).items():
            c1 = n.startswith('Key_')
            c2 = n.endswith('Modifier')
            if c1 or c2: 
                if c1: 
                    n=n.replace('Key_', '').lower()
                self.key_map[v]=n

    def executeMatch(
            self, 
            matches, 
            partial, 
            digit
            ):

        if not partial:
            if len(matches)<2: 
                self.clearKeys()
            if len(matches)==1:
                m=matches[0]
                self.runBeforeExecute()
                f=getattr(m, '__wrapped__', m)
                c1='digit' in signature(f).parameters
                if digit is not None and c1: 
                    m(digit=digit)
                else:
                    m()
                self.runAfterExecute()

    def runAfterExecute(self): 
        self.matchIsExecuted.emit()

    def runBeforeExecute(self): 

        self.clearKeys()
        self.matchIsToBeExecuted.emit()
        d=getattr(
                self.obj, 
                'delisten_on_exec', 
                self.delisten_on_exec)
        w=getattr(
                self.obj,
                'mode_on_exit',
                self.mode_on_exit)
        if d: 
            self.obj.deactivate()
            self.app.moder.modeWanted.emit(w)

    def parseMode(self, mode):

        t=mode.split('|')
        if len(t)==1:
            return t[0], ['default']
        elif len(t)==2:
            return t[0], t[1].split(':')
