from PyQt5 import QtCore 
from inspect import signature

from qplug import PlugObj
from qplug.utils import register

class Mode(PlugObj):

    def __init__(self, 
                 wait_run=2,
                 wait_time=100,
                 report_keys=True,
                 delisten_on_exec=True,
                 mode_on_exit='normal',
                 **kwargs):

        self.commands={}
        self.keys_pressed=[]
        self.wait_run=wait_run
        self.wait_time=wait_time
        self.report_keys=report_keys
        self.mode_on_exit=mode_on_exit

        self.delisten_on_exec=delisten_on_exec

        super(Mode, self).__init__(
                command_leader=[], 
                **kwargs)

    def setup(self):

        super().setup()
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.deactivate)

    def saveCommands(self, plug, method):

        prefix=plug.modeKey(self.name)
        key=f'{prefix}{method.key}'
        self.commands[key]=method

    def setPlugData(self):

        def setData(plug, actions, mname=None):

            for (pname, fname), m in actions.items():
                if not mname or  mname in m.modes:
                    if hasattr(m, 'key'): 
                        self.saveCommands(plug, m)

        for plug, actions in self.app.manager.actions.items():
            setData(plug, actions, self.name)

        own_actions=self.app.manager.actions.get(self)
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

    def checkSpecialCharacters(self, event):

        enter=[QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]

        if event.key() in enter: 

            self.on_returnPressed()
            return 'return'
                
        elif event.key()==QtCore.Qt.Key_Backspace:

            self.on_backspacePressed()
            return 'backspace'

        elif event.key()==QtCore.Qt.Key_Escape:

            self.on_escapePressed()
            return 'escape'

        elif event.key()==QtCore.Qt.Key_Tab:

            self.on_tabPressed()
            return 'tab'

        elif event.modifiers()==QtCore.Qt.ControlModifier:

            if event.key()==QtCore.Qt.Key_BracketLeft:
                self.on_escapePressed()
                return 'escape_bracket'

            elif event.key()==QtCore.Qt.Key_M:
                self.on_carriagePressed()
                return 'carriage'

        return False

    def clearKeys(self):

        self.timer.stop()
        self.keys_pressed=[]

    def listen(self):

        super().listen()
        self.clearKeys()

    def delisten(self):

        super().delisten()
        self.timer.stop()
        self.clearKeys()

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

            if self.report_keys:
                self.bar_data={
                        'detail': ''.join(self.keys_pressed)}
            else:
                self.bar_data={}

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
            self.modeWanted.emit(self.mode_on_exit)

    @register('q')
    def exit(self): self.app.exit()

    def on_carriagePressed(self): pass

    def on_tabPressed(self): pass

    def on_escapePressed(self): 

        if self.delisten_on_exec: 
            self.modeWanted.emit(self.mode_on_exit)
        else:
            self.delistenWanted.emit()

    def on_returnPressed(self): self.returnPressed.emit()

    def on_backspacePressed(self): self.clearKeys()
