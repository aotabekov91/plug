from plug import utils
from PyQt5.QtCore import QObject, pyqtSignal

class Moder(utils.Moder, QObject):

    delistenWanted=pyqtSignal()
    plugAdded=pyqtSignal(object)
    modeWanted=pyqtSignal(object)
    typeWanted=pyqtSignal(object)
    typeChanged=pyqtSignal(object)
    viewWanted=pyqtSignal(object)
    viewChanged=pyqtSignal(object)
    modeChanged=pyqtSignal(object)
    plugsLoaded=pyqtSignal(object)
    modeIsToBeSet=pyqtSignal(object)
    actionsRegistered=pyqtSignal(object, object)

    def setup(self):

        super().setup()
        self.modeWanted.connect(
                self.setMode)
        self.typeWanted.connect(
                self.setType)
        # self.viewWanted.connect(
        #         self.setView)
        self.delistenWanted.connect(
                self.setMode)
        self.app.uiman.appLaunched.connect(
                self.launch)
        self.app.uiman.viewActivated.connect(
                self.setView)
        self.app.uiman.viewOctivated.connect(
                self.setDefaultView)

    def setDefaultView(self):

        v=None
        t=self.m_type
        if t: v=t.view()
        m=self.current
        dv=getattr(m, 'defaultView', None)
        if dv: v=dv()
        self.setView(v)

    def setView(self, v):

        super().setView(v)
        if v: v.setFocus()
        self.viewChanged.emit(v)

    def setType(self, t):

        super().setType(t)
        self.typeChanged.emit(t)

    def launch(self):

        self.setMode(self.default)
        w=getattr(self.app, 'window', None)
        if w: w.focusGained.connect(self.reset)

    def reset(self):
        self.setMode(self.current)

    def add(self, plug):

        super().add(plug)
        self.plugAdded.emit(plug)

    def load(self, *args, **kwargs):

        super().load(*args, **kwargs)
        self.plugsLoaded.emit(self.plugs)

    def setMode(self, mode=None):

        m=self.getMode(mode)
        self.modeIsToBeSet.emit(m)
        m=super().setMode(m)
        if m: self.modeChanged.emit(m)
        return m

    def save(self, plug, actions):

        super().save(plug, actions)
        self.actionsRegistered.emit(plug, actions)
