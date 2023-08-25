from PyQt5 import QtCore
from inspect import signature

# PlugObj: checkListen, checkMode, eventFilter, listen, delisten
# Mode:  > EventListener
# PlugObj.event_listner=EventListner(PlugObj)
# Plug: eventFilter, setLeaders, checkKey, [de]activateCommandMode, modeKey

class EventListener(QtCore.QObject):

    keyPressed=QtCore.pyqtSignal(object, object)
    # todo: set parent's config keys if provided

    def __init__(self, 
                 obj=None,
                 config={},
                 wait_run=10,
                 wait_time=100,
                 mode_on_exit='normal',
                 delisten_on_exec=True,
                 ):

        super().__init__(obj)

        self.obj=obj
        self.commands={}
        self.config=config
        self.listening=False
        self.keys_pressed=[]
        self.wait_run=wait_run
        self.wait_time=wait_time
        self.timer=QtCore.QTimer()
        self.mode_on_exit=mode_on_exit
        self.delisten_on_exec=delisten_on_exec

        self.setup()

    def setup(self):

        self.setObj()
        self.saveKeys()

        self.timer.timeout.connect(
                lambda: self.executeMatch([], [], 0))

    def clearKeys(self):

        self.timer.stop()
        self.keys_pressed=[]

    def eventFilter(self, widget, event):

        if event.type()==QtCore.QEvent.KeyPress:
            return self.addKeys(event)
        return False

    def setObj(self):

        if hasattr(self.obj, 'keyPressed'):
            self.obj.keyPressed.connect(self.keyPressed)
        self.obj.installEventFilter(self)

    def addKeys(self, event):

        self.timer.stop()
        matches, partial = [], []
        if self.registerKey(event):
            key, digit = self.getKeys()
            self.keyPressed.emit(digit, key)
            matches, partial=self.getMatches(tuple(key), digit)
            self.runMatches(matches, partial, key, digit)

        if matches or partial:
            return True
        else:
            self.keys_pressed=[]
            return False

    def registerKey(self, event):
        
        mod=[]
        mdf=event.modifiers()
        if (mdf & QtCore.Qt.AltModifier):
            mod+=[QtCore.Qt.AltModifier]
        if (mdf & QtCore.Qt.ControlModifier):
            mod+=[QtCore.Qt.ControlModifier]
        if mdf & QtCore.Qt.ShiftModifier:
            mod+=[QtCore.Qt.ShiftModifier]

        text=event.text()

        if text and text.isnumeric():
            mod+=[text]
        else:
            mod+=[event.key()]

        if mod and event.text():
            self.keys_pressed+=mod
        return mod

    def getKeys(self):

        key, digit = [], ''
        for i, k in enumerate(self.keys_pressed):
            if type(k)==str:
                digit+=k
            else:
                key=self.keys_pressed[i:]
                break
        if digit: 
            digit=int(digit)
        else:
            digit=None
        return key, digit

    def getMatches(self, key, digit):

        m, p = [], []
        for k, f in self.commands.items():
            if key==k[:len(key)]: 
                if digit:
                    t=getattr(f, '__wrapped__', f)
                    c1='digit' in signature(t).parameters
                    if not c1: continue
                if key==k: 
                    m+=[f]
                elif key==k[:len(key)]: 
                    p+=[f]
        return m, p

    def runMatches(self, matches, partial, key, digit):

        self.timer.timeout.disconnect()
        self.timer.timeout.connect(
                lambda: self.executeMatch(
                    matches, partial, digit))
        if len(matches)==1 and not partial:
            self.timer.start(self.wait_run)
        else:
            if self.wait_time: 
                self.timer.start(self.wait_time)

    def executeMatch(self, matches, partial, digit):

        if not partial:
            if len(matches)<2: 
                self.clearKeys()
            if len(matches)==1:
                m=matches[0]
                f=getattr(m, '__wrapped__', m)
                c1='digit' in signature(f).parameters

                if digit and c1: 
                    m(digit=digit)
                else:
                    m()

    def saveKeys(self):

        mapping={
                ',': 'Comma', 
                ';': 'Semicolon', 
                '.': 'Period'
                }

        for f in self.obj.__dir__():
            m=getattr(self.obj, f)
            if hasattr(m, 'key'):
                key=m.key
                #todo: 'Shift+e Ctrl+a'
                match=[]
                s=key.split(' ')
                for j in s:
                    for i in j.split('+'):
                        if i=='Ctrl':
                            match+=[getattr(
                                QtCore.Qt,'ControlModifier')]
                        elif i=='Alt':
                            match+=[getattr(
                                QtCore.Qt,'AltModifier')]
                        elif i=='Shift':
                            match+=[getattr(
                                QtCore.Qt,'ShiftModifier')]
                        else:
                            k=mapping.get(i, i.upper())
                            v=getattr(QtCore.Qt, f"Key_{k}", k)
                            match+=[v]
                self.commands[tuple(match)]=m
                # print(key, match)

class SetKeys(type(QtCore.QObject)):

    def __call__(cls, *args, **kwargs):

        def setListener(obj, listener):
            pass

        obj=type.__call__(cls, *args, **kwargs)
        obj.listener=Listener(obj)
        obj.setListener=
        return obj
