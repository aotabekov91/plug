from PyQt5 import QtCore
from inspect import signature

# Mode:  > EventListener

class EventListener(QtCore.QObject):

    escapePressed=QtCore.pyqtSignal()
    returnPressed=QtCore.pyqtSignal()
    backspacePressed=QtCore.pyqtSignal()

    forceDelisten=QtCore.pyqtSignal()
    delistenWanted=QtCore.pyqtSignal()
    modeWanted=QtCore.pyqtSignal(object)
    listenWanted=QtCore.pyqtSignal(object)
    keyPressed=QtCore.pyqtSignal(object, object)

    def __init__(
            self, 
            app=None, 
            obj=None, 
            config={},
            wait_run=10,
            wait_time=100,
            listen_leader=None, 
            command_leader=None,
            mode_on_exit='normal',
            delisten_on_exec=True,
            ):

        super().__init__(obj)

        self.obj=obj
        self.app=app
        self.commands={}
        self.config=config
        self.listening=False
        self.keys_pressed=[]
        self.wait_run=wait_run
        self.wait_time=wait_time
        self.timer=QtCore.QTimer()
        self.mode_on_exit=mode_on_exit
        self.listen_leader=listen_leader
        self.command_leader=command_leader
        self.delisten_on_exec=delisten_on_exec

        self.setup()

    def setObj(self):

        if hasattr(self.obj, 'keyPressed'):
            self.keyPressed.connect(
                    self.obj.keyPressed)
        if hasattr(self.obj, 'command_leader'):
            self.command_leader=self.parseKey(
                    self.obj.command_leader)
        if hasattr(self.obj, 'listen_leader'):
            self.listen_leader=self.parseKey(
                    self.obj.listen_leader)
        if hasattr(self.obj, 'forceDelisten'):
            self.forceDelisten.connect(
                    self.obj.forceDelisten)
        if hasattr(self.obj, 'delistenWanted'):
            self.delistenWanted.connect(
                    self.obj.delistenWanted)
        if hasattr(self.obj, 'modeWanted'):
            self.modeWanted.connect(
                    self.obj.modeWanted)
        if hasattr(self.obj, 'listenWanted'):
            self.listenWanted.connect(
                    self.obj.listenWanted)
        if hasattr(self.obj, 'returnPressed'):
            self.returnPressed.connect(
                    self.obj.returnPressed)

        obj=self.obj
        if self.app: obj=self.app
        obj.installEventFilter(self)

    def setup(self):

        self.setObj()
        self.saveKeys()

        self.timer.timeout.connect(
                lambda: self.executeMatch(
                    [], [], 0))
        # self.timer.timeout.connect(self.obj.deactivate)

        self.backspacePressed.connect(self.clearKeys)
        self.escapePressed.connect(self.on_escapePressed)

    def on_escapePressed(self): 

        if self.delisten_on_exec: 
            self.modeWanted.emit(self.mode_on_exit)
        else:
            self.delistenWanted.emit()

    def clearKeys(self):

        self.timer.stop()
        self.keys_pressed=[]

    def eventFilter(self, widget, event):

        if event.type()==QtCore.QEvent.KeyPress:

            if self.listening: 
                if self.checkMode(event):
                    event.accept()
                    return True
                elif self.command_leader:
                    c=hasattr(self, 'ui') 
                    c=c and hasattr(self.ui, 'commands')
                    if c:
                        c1=self.checkLeader(event, 'command_leader')
                        if c1:
                            self.obj.toggleCommandMode()
                            event.accept()
                            return True
            return self.addKeys(event)
        return False

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

    def getPressed(self, event):

        pressed=[]
        mdf=event.pressedifiers()
        if (mdf & QtCore.Qt.AltModifier):
            pressed+=[QtCore.Qt.AltModifier]
        if (mdf & QtCore.Qt.ControlModifier):
            pressed+=[QtCore.Qt.ControlModifier]
        if mdf & QtCore.Qt.ShiftModifier:
            pressed+=[QtCore.Qt.ShiftModifier]
        text=event.text()
        if text and text.isnumeric():
            pressed+=[text]
        else:
            pressed+=[event.key()]
        return pressed

    def registerKey(self, event):

        pressed=self.getPressed(event)
        if pressed and event.text():
            self.keys_pressed+=pressed
        return pressed

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

        for f in self.obj.__dir__():
            m=getattr(self.obj, f)
            if hasattr(m, 'key'):
                match=self.parseKey(m.key)
                self.commands[tuple(match)]=m

    def parseKey(self, key):

        mapping={
                ',': 'Comma', 
                ';': 'Semicolon', 
                '.': 'Period'
                }

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
        return match
    
    def checkLeader(self, event, kind='listen_leader'):

        pressed=self.getPressed(event)
        if kind=='listen_leader':
            check_val=self.listen_leader
        elif kind=='command_leader':
            check_val=self.command_leader
        if pressed==check_val: 
            return True
        else:
            return False

    def checkMode(self, event):

        if self.app:
            ms=self.app.plugman.getModes().items()
            for _, m in ms:
                if m.checkLeader(event, kind='listen_leader'): 
                    if m==self:
                        self.delistenWanted.emit()
                    else:
                        self.modeWanted.emit(m)
                    return True
        return False

    def listen(self):

        self.listening=True
        self.clearKeys()

    def delisten(self):

        self.listening=False
        self.timer.stop()
        self.clearKeys()

    def checkSpecialCharacters(self, event):

        enter=[QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]
        if event.key() in enter: 
            self.returnPressed.emit()
            return 'return'
        elif event.key()==QtCore.Qt.Key_Backspace:
            self.backspacePressed.emit()
            return 'backspace'
        elif event.key()==QtCore.Qt.Key_Escape:
            self.escapePressed.emit()
            return 'escape'
        elif event.key()==QtCore.Qt.Key_Tab:
            self.tabPressed.emit()
            return 'tab'
        elif event.modifiers()==QtCore.Qt.ControlModifier:
            if event.key()==QtCore.Qt.Key_BracketLeft:
                self.escapePressed.emit()
                return 'escape_bracket'
            elif event.key()==QtCore.Qt.Key_M:
                self.carriageReturnPressed.emit()
                return 'carriage'
        return False
