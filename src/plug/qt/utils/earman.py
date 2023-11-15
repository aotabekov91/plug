import re
from PyQt5 import QtCore 
from inspect import signature
from PyQt5.QtWidgets import QWidget, QTextEdit, QLineEdit

class EarMan(QtCore.QObject):

    wait_run=5
    wait_time=200
    default_mode='normal'
    delisten_on_exec=False
    delisten_key=[QtCore.Qt.Key_Escape]
    keysChanged=QtCore.pyqtSignal(object)

    mapping={
            ',': 'Comma', 
            ';': 'Semicolon', 
            '.': 'Period',
            '-': 'Minus',
            '.': 'Period',
            '/': 'Slash',
            '+': 'Plus',
            '*': 'Asterisk',
            '@': 'At',
            '$': 'Dollar',
            '[': 'BracketLeft',
            ']': 'BracketRight',
            '_': 'Underscore',
            ' ': 'Space'}

    def __init__(self, app):

        self.app=app
        self.keys={}
        self.obj=None
        self.kwargs={}
        self.leaders={}
        self.commands={}
        self.ptext=''
        self.pkeys=[]
        super().__init__(app)
        self.app.moder.plugsLoaded.connect(
                self.setPlugs)
        self.app.qapp.installEventFilter(
                self)
        self.setKeyMap()
        self.setTimer()

    def setTimer(self):

        self.timer=QtCore.QTimer()
        f=lambda: self.executeMatch([], [], 0)
        self.timer.timeout.connect(f)
        self.timer.setSingleShot(True)

    def listen(self, obj):
        self.obj=obj

    def delisten(self, obj):
        self.obj=None

    def setPlugs(self, plugs):

        self.createHolders(plugs)
        self.setPlugActions(plugs)
        self.setPlugLeaders(plugs)

    def setPlugLeaders(self, plugs):

        for p in plugs.values():
            l=getattr(p, 'listen_leader', None)
            if l:
                k=self.parseKey(l)
                self.leaders[k]=p

    def setPlugActions(self, plugs):

        for n, p in plugs.items():
            self.setActions(p)
            self.setUIActions(p)

    def setUIActions(self, p):

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
                    raise

            if key: 
                k[w]=key
            if command: 
                c[w]=command

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
            self.keys[p]={'default': {}}
            self.commands[p]={'default': {}}

    def setActions(self, obj):

        k=self.keys[obj]
        c=self.commands[obj]
        acs=self.app.moder.actions
        for o, a in acs.items():
            for (pn, n), m in a.items():
                any_='any' in m.modes
                in_=obj.name in m.modes
                own_=o==obj and len(m.modes)==0
                if not any([own_, any_, in_]):
                    continue
                key=self.setKey(obj, o, m, n)
                c['default'][n]=m
                if key: k['default'][key]=m

    def setKey(self, obj, o, m, n):

        k=getattr(m, 'key')
        if k:
            l=getattr(o, 'leader_keys', {})
            p=l.get(obj.name, '')
            return self.parseKey(k, prefix=p)

    def parseKey(self, key, prefix=''):

        def parseLetter(t):

            unit=[]
            if t.isupper(): 
                unit+=[getattr(QtCore.Qt,'ShiftModifier')]
            k=self.mapping.get(t, t.upper())
            unit+=[getattr(QtCore.Qt, f"Key_{k}")]
            return unit

        def parse(key):

            parsed=[]
            p=r'(?P<group>(<[acAC]-.>)*)(?P<tail>([^<]*))'
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
        elif hasattr(self.obj, 'suffix_functor'):
            return self.obj.suffix_functor(e)
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
        self.pressed=None
        self.ptext=''
        self.pkeys=[]

    def checkLeader(self, e):

        for l, p in self.leaders.items():
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

        def getWKeys(w):

            if w==self.obj.ui or w in keys:
                return keys.get(w, {})
            return getWKeys(w.parent())

        def addWidgetKeys(l):

            ui=getattr(self.obj, 'ui', None)
            if ui:
                w=self.app.qapp.focusWidget()
                edits=[QTextEdit, QLineEdit]
                mdfs=e.modifiers()
                c1=not type(w) in edits
                c2=mdfs & QtCore.Qt.ControlModifier
                if c1 or c2: 
                    ch=ui.findChildren(QWidget)
                    ch.append(ui)
                    if w in ch: 
                        l+=[getWKeys(w)]

        m, p = [], []
        keys=self.keys.get(self.obj, {})
        l=[keys.get('default', {})]
        addWidgetKeys(l)

        for i in l:
            for v, f in i.items():
                for c in v:
                    if k!=c[:len(k)]: continue
                    if not d is None:
                        t=getattr(f, '__wrapped__', f)
                        c1='digit' in signature(t).parameters
                        if not c1: continue
                    if k==c: 
                        m+=[f]
                    elif k==c[:len(k)]: 
                        p+=[f]
        return m, p

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
                if shift: 
                    n=n.upper()
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
                self.on_executeMatch()
                f=getattr(m, '__wrapped__', m)
                c1='digit' in signature(f).parameters
                if digit is not None and c1: 
                    m(digit=digit)
                else:
                    m()

    def on_executeMatch(self): 

        d=getattr(
                self.obj, 
                'delisten_on_exec', 
                self.delisten_on_exec)
        w=getattr(
                self.obj,
                'mode_on_exit',
                self.default_mode)
        if d: 
            self.keysChanged.emit('')
            self.app.moder.modeWanted.emit(w)

    def isListening(self, obj):
        return self.obj==obj