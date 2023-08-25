from PyQt5 import QtCore 
from inspect import signature

from plug.qt import PlugObj
from plug.qt.utils import register

class Mode(PlugObj):

    keysChanged=QtCore.pyqtSignal(str)

    def __init__(self, 
                 wait_run=2,
                 wait_time=100,
                 delisten_on_exec=True,
                 mode_on_exit='normal',
                 **kwargs):

        self.commands={}
        self.keys_pressed=[]
        self.wait_run=wait_run
        self.wait_time=wait_time
        self.mode_on_exit=mode_on_exit
        self.delisten_on_exec=delisten_on_exec

        super(Mode, self).__init__(
                command_leader=[], 
                **kwargs)

    def saveCommands(self, plug, method, key):

        if hasattr(plug, 'mode_key'):
            prefix=plug.mode_key.get(self.name, None)
            if prefix: key=f'{prefix} {key}'
        self.commands[key]=method

    def setPlugData(self):

        def setData(plug, actions, mname=None):

            for (pname, fname), m in actions.items():
                if not mname or  mname in m.modes:
                    if hasattr(m, 'key'): 
                        key=m.key
                    else:
                        key=None
                    self.saveCommands(plug, m, key)

        for plug, actions in self.app.plugman.actions.items():
            setData(plug, actions, self.name)

        own_actions=self.app.plugman.actions.get(self)
        if own_actions: setData(self, own_actions)

    def eventFilter(self, widget, event):

        c1=event.type()==QtCore.QEvent.KeyPress

        if self.listening and c1: 

            if self.checkSpecialCharacters(event):
                event.accept()
                return True
            else:
                mode=self.checkListen(event)
                if not mode:
                    self.addKeys(event, widget)
                    event.accept()
                    return True
        return super().eventFilter(widget, event)


    def addKeys(self, event, widget=None):

        self.timer.stop()
        if self.registerKey(event):
            key, digit = self.getKeys()
            self.keyPressed.emit(digit, key)
            matches, partial=self.getMatches(key, digit)
            self.runMatches(matches, partial, key, digit)

    def registerKey(self, event):
        
        text=event.text()
        if text: 
            self.keys_pressed+=[text]
            pressed=''.join(self.keys_pressed)
            self.keysChanged.emit(pressed)
        return text

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

    def getKeys(self):

        key, digit = '', ''

        for i, k in enumerate(self.keys_pressed):
            if k.isnumeric():
                digit+=k
            else:
                key=''.join(self.keys_pressed[i:])
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

    def executeMatch(self, matches, partial, digit):

        if not partial:

            if len(matches)<2: 
                self.clearKeys()

            if len(matches)==1:
                self._onExecuteMatch()

                m=matches[0]

                f=getattr(m, '__wrapped__', m)
                c1='digit' in signature(f).parameters

                if digit and c1: 
                    m(digit=digit)
                else:
                    m()

    def _onExecuteMatch(self): 

        if self.delisten_on_exec: 
            self.keysChanged.emit('')
            self.modeWanted.emit(self.mode_on_exit)
