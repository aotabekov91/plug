import re
from PyQt5 import QtCore 
from inspect import signature

class EarMan(QtCore.QObject):

    wait_run=5
    wait_time=200
    mode_on_exit='normal'
    delisten_on_exec=False
    delisten_key_=['<escape>', '<c-['] # Todo
    delisten_key=[QtCore.Qt.Key_Escape]
    matchIsExecuted=QtCore.pyqtSignal()
    objectAdded=QtCore.pyqtSignal(object)
    keysChanged=QtCore.pyqtSignal(object)
    matchIsToBeExecuted=QtCore.pyqtSignal()
    pttr=r'(?P<m>([^[]*))(\[(?P<s>([^]]*))\])*'

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

        super().__init__(app)
        self.app=app
        self.m_ptext=''
        self.m_keys={}
        self.m_modes={}
        self.m_pkeys=[]
        self.m_obj=None
        self.setTimer()
        self.setKeyMap()
        self.m_methods={}
        self.m_leaders={}
        self.m_prefixes={}
        self.m_passive=False
        self.m_passive_modes=[]
        self.app.qapp.installEventFilter(
                self)
        self.app.moder.plugAdded.connect(
                self.addPlug)
        self.app.handler.viewAdded.connect(
                self.addView)

    def obj(self):
        return self.m_obj

    def setPassive(self, cond=False, modes=[]):

        modes.append('any')
        self.m_passive=cond
        self.m_passive_modes=modes
        self.clearKeys()
        self.keysChanged.emit('')

    def addView(self, view):

        self.setLeader(view)
        self.setObjKeys(
                view, view=True)
        self.updateObjKeys()
        self.addAnyKeys()
        self.objectAdded.emit(view)

    def addPlug(self, plug):

        self.m_modes[plug.name]=plug
        d=(plug.name, None, None, None)
        if not d in self.m_keys:
            self.m_keys[d]={}

        self.setLeader(plug)
        self.setObjKeys(plug)
        self.updateObjKeys()
        self.addAnyKeys()
        self.objectAdded.emit(plug)

    def updateObjKeys(self):

        for s, d in self.m_keys.items():
            data={}
            ms=[None, None, None, None]
            for i in range(3):
                ms[i]=s[i]
                tk=self.m_keys.get(
                        tuple(ms), {})
                data.update(tk)
            data.update(d)
            self.m_keys[s]=data
                
    def addAnyKeys(self):
        
        any_mode=self.m_keys.get(
                ('any', None, None, None), None)
        if any_mode:
            for d in self.m_keys.values():
                d.update(any_mode)

    def setLeader(self, o):

        l=getattr(o, 'listen_leader', None)
        if l:
            k=self.parseKey(l)
            self.m_leaders[k]=o

    def parseKeyMode(self, m):

        s=m.split('|')
        mode, view = None, None
        i, j, k, l = None, None, None, None
        if len(s)==2:
            mode, view=s[0], s[1]
        elif len(s)==1:
            mode=s[0]
        if mode:
            r=re.match(self.pttr, mode)
            i=r.group('m')
            j=r.group('s')
        if view:
            r=re.match(self.pttr, view)
            k=r.group('m')
            l=r.group('s')
        if i:
            yield (i, j, k, l)
        else:
            for m in self.m_modes:
                yield (m, j, k, l)

    def setPrefixKeys(self, o):

        if not o in self.m_prefixes:
            self.m_prefixes[o]={}
        l=getattr(o, 'prefix_keys', {})
        for n, k in l.items():
            for r in self.parseKeyMode(n):
                self.m_prefixes[o][r]=k
        return (o, l)

    def setObjKeys(self, o, view=False):

        pn=[]
        self.setPrefixKeys(o)
        p=self.m_prefixes[o]
        for i in o.__class__.__mro__[::-1]:
            pn+=[i.__name__]
        for f in o.__dir__():
            func=getattr(o, f)
            # k=getattr(func, 'key', '') # quickfix
            t=getattr(func, 'isTagged', None)
            if not t: continue
            k=getattr(func, 'key', '')
            m=getattr(func, 'modes', [])
            # if not k: continue
            # if m is None: continue
            # if k is None: continue
            m = m or [o.name]
            for i in m: 
                i=i.replace('^own', o.name)
                if not i in self.m_methods:
                    self.m_methods[i]=[]
                self.m_methods[i]+=[func]
                for r in self.parseKeyMode(i):
                    s=None
                    if r[2] in pn and view:
                        s=list(r)
                        s[2]=o.name
                        s=tuple(s)
                        if not s in self.m_keys:
                            self.m_keys[s]={}
                    if not r in self.m_keys:
                        self.m_keys[r]={}
                    pref=p.get(r, '')
                    parsedk=self.parseKey(k, pref)
                    for pk in parsedk: 
                        self.m_keys[r][(o, pk)]=func
                        if not s: continue
                        self.m_keys[s][(o, pk)]=func
        
    def setTimer(self):

        self.timer=QtCore.QTimer()
        f=lambda: self.execute([], [], 0)
        self.timer.timeout.connect(f)
        self.timer.setSingleShot(True)

    def listen(self, obj):
        self.m_obj=obj

    def delisten(self, obj):
        self.m_obj=None

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

        if not key: return () 
        if type(key)==str: 
            key=[key]
        p=[]
        for k in key: 
            p+=[parse(f"{prefix}{k}")]
        return tuple(p)

    def eventFilter(self, w, e):

        if not self.m_obj:
            return False
        if e.type()!=QtCore.QEvent.KeyPress:
            return False
        no_partial=len(self.m_pkeys)==0
        self.registerKey(e)
        if no_partial and self.checkLeader(e) :
            e.accept()
            return True
        if self.addKeys(e):
            e.accept()
            return True
        elif hasattr(self.m_obj, 'event_functor'):
            r=self.m_obj.event_functor(e, self)
            if r:
                e.accept()
                return True
        self.clearKeys()
        self.keysChanged.emit('')
        return False

    def registerKey(self, e):

        self.pressed=self.getPressed(e)
        if self.pressed and e.text():
            t=self.getText(self.pressed)
            self.m_ptext+=t
            self.m_pkeys.append(self.pressed)
            self.keysChanged.emit(self.m_ptext)

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
        self.m_ptext=''
        self.m_pkeys=[]
        self.pressed=None

    def checkLeader(self, e):

        for l, p in self.m_leaders.items():
            if self.m_passive and p!=self.m_obj:
                continue
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
        c1 = not self.m_passive
        c2 = e.key() in self.delisten_key
        if c1 and c2: 
            self.clearKeys()
            self.m_obj.octivate()
            return True
        elif self.pressed:
            m, p = [], []
            k, d = self.getKeys()
            m, p = self.match(k, d, e)
            self.run(m, p, k, d)
            return m or p

    def getKeys(self):

        key, digit = [], ''
        for i, k in enumerate(self.m_pkeys):
            p=self.key_map[k[0]]
            if p.isnumeric():
                digit+=p
            else:
                key=self.m_pkeys[i:]
                break
        if digit: 
            digit=int(digit)
        else:
            digit=None
        return tuple(key), digit

    def getStateKeys(self, state):

        if state in self.m_keys:
            return self.m_keys[state]
        ms=list(state)
        for i in range(3, -1, -1):
            ms[i]=None
            k=self.m_keys.get(
                    tuple(ms), None)
            if k: return k
        return {}

    def getState(self):

        m=self.app.handler.mode()
        v=self.app.handler.view()
        f=self.app.handler.type()
        sm=self.app.handler.submode()
        mn=None
        if m: mn=m.name
        sn=None
        if sm and hasattr(sm, 'name'):
            sn=sm.name
        elif sm and type(sm)==str:
            sn=sm
        vn=None
        if v: vn=v.name
        fn=None
        if f: fn=f.kind
        if self.m_passive:
            if not mn in self.m_passive_modes:
                return ('any', None, None, None)
        return (mn, sn, vn, fn)

    def match(self, k, d, e):

        m, p = [], []
        s=self.getState()
        skeys=self.getStateKeys(s)
        for (so, sk), sf in skeys.items():
            if d is not None:
                c='digit' in signature(sf).parameters
                if not c: continue
            if k!=sk[:len(k)]: continue
            if k==sk: 
                m+=[sf]
            elif k==sk[:len(k)]: 
                p+=[sf]
        return m, p

    def run(self, m, p, k, d):

        t=self.timer
        t.timeout.disconnect()
        f=lambda: self.execute(m, p, d)
        t.timeout.connect(f)
        w=self.wait_time
        if len(m)==1 and not p:
            w=self.wait_run
        t.start(w)

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

    def execute(
            self, 
            matches, 
            partial, 
            digit
            ):

        if not partial and len(matches)==1:
            m=matches[0]
            self.runBefore()
            f=getattr(m, '__wrapped__', m)
            c1='digit' in signature(f).parameters
            if digit is not None and c1: 
                m(digit=digit)
            else:
                m()
            self.runAfter()

    def runAfter(self): 

        self.clearKeys()
        self.matchIsExecuted.emit()

    def runBefore(self): 

        self.matchIsToBeExecuted.emit()
        d=getattr(
                self.m_obj, 
                'delisten_on_exec', 
                self.delisten_on_exec)
        w=getattr(
                self.m_obj,
                'mode_on_exit',
                self.mode_on_exit)
        if d: 
            self.m_obj.octivate()
            self.app.moder.modeWanted.emit(w)
