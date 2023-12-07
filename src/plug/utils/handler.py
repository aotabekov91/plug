from PyQt5 import QtCore

class Handler(QtCore.QObject):

    viewAdded=QtCore.pyqtSignal(object)
    typeAdded=QtCore.pyqtSignal(object)
    typerAdded=QtCore.pyqtSignal(object)
    viewWanted=QtCore.pyqtSignal(object)
    modelAdded=QtCore.pyqtSignal(object)
    typeWanted=QtCore.pyqtSignal(object)
    viewClosed=QtCore.pyqtSignal(object)
    modeChanged=QtCore.pyqtSignal(object)
    viewChanged=QtCore.pyqtSignal(object)
    typeChanged=QtCore.pyqtSignal(object)
    viewerAdded=QtCore.pyqtSignal(object)
    viewCreated=QtCore.pyqtSignal(object)
    modelLoaded=QtCore.pyqtSignal(object)
    modelCreated=QtCore.pyqtSignal(object)
    modellerAdded=QtCore.pyqtSignal(object)
    submodeChanged=QtCore.pyqtSignal(object)

    def __init__(self, app, config):

        super().__init__(app)
        self.app=app
        self.m_mode=None
        self.m_type=None
        self.m_view=None
        self.m_typers=[]
        self.m_viewers=[]
        self.m_modellers=[]
        self.m_submode=None
        self.m_config=config
        self.uiman=self.app.uiman
        self.buffer=self.app.buffer
        self.setup()

    def setup(self):

        self.setSettings()
        self.typeWanted.connect(self.setType)
        self.viewWanted.connect(self.setView)
        self.app.moder.modeChanged.connect(
                self.setMode)
        self.app.moder.submodeChanged.connect(
                self.setSubmode)

    def setDefaultView(self):

        m=self.mode()
        v=self.app.display.currentView()
        df=getattr(m, 'getDefaultView', None)
        if df: v=df()
        if v: v.setFocus()

    def setView(self, v):

        self.m_view=v
        self.viewChanged.emit(v)
        if not v: return
        m=v.model()
        if m and m.isType: 
            self.setType(v) 

    def setMode(self, m):

        self.m_mode=m
        self.modeChanged.emit(m)

    def setSubmode(self, s):

        self.m_submode=s
        self.submodeChanged.emit(s)

    def setType(self, v):

        self.m_type=v
        self.typeChanged.emit(v)

    def type(self):
        return self.m_type

    def view(self):
        return self.m_view

    def mode(self):
        return self.m_mode

    def submode(self):
        return self.m_submode

    def setSettings(self):

        s=self.m_config.get('Settings', {})
        for n, v in s.items():
            setattr(self, n, v)

    def addViewer(self, v):

        if not v in self.m_viewers:
            self.m_viewers+=[v]
            self.viewerAdded.emit(v)

    def viewers(self):
        return self.m_viewers

    def addModeller(self, m):

        if not m in self.m_modellers:
            self.m_modellers+=[m]
            self.modellerAdded.emit(m)

    def modellers(self):
        return self.m_modellers

    def addTyper(self, v):

        if not v in self.m_typers:
            self.m_typers+=[v]
            self.typerAdded.emit(v)

    def typers(self):
        return self.m_typers

    def getModel(self, source, **kwargs):

        for k in self.m_modellers:
            if not k.isCompatible(source, **kwargs):
                continue
            n=k.getSourceName(source, **kwargs)
            m=self.buffer.getModel(n)
            if not m:
                sc=self.getConfig(k)
                gc=kwargs.get('config', {})
                gc.update(sc)
                kwargs['config']=gc
                m=k(source=source, **kwargs)
                self.buffer.setModel(n, m)
                m.load()
            m.resetConfigure(source=source, **kwargs)
            self.modelCreated.emit(m)
            if hasattr(m, 'loaded'):
                m.loaded.connect(self.modelLoaded)
            return m

    def getView(self, model, **kwargs):

        v=self.buffer.getView(model)
        if v and model.wantUniqView:
            v.resetConfigure(model=model, **kwargs)
            return v
        else:
            for k in self.m_viewers:
                if not k.isCompatible(model, **kwargs):
                    continue
                sc=self.getConfig(k)
                gc=kwargs.get('config', {})
                gc.update(sc)
                kwargs['config']=gc
                v=k(app=self.app, **kwargs)
                v.setModel(model=model)
                self.buffer.setView(model, v)
                self.uiman.setupUI(
                        ui=v, name=v.name)
                if model.isType:
                    self.typeAdded.emit(v)
                self.connectView(v)
                v.resetConfigure(model=model, **kwargs)
                self.viewCreated.emit(v)
                return v

    def connectView(self, v):

        self.viewAdded.emit(v)
        if hasattr(v, 'activateWanted'):
            v.focusGained.connect(self.setView)
            v.activateWanted.connect(self.activateView)
            v.octivateWanted.connect(self.octivateView)

    def activateView(self, v, **kwargs):
        self.uiman.activate(ui=v, **kwargs)

    def octivateView(self, v, **kwargs):

        self.setDefaultView()
        self.uiman.octivate(ui=v, **kwargs)

    def handleInitiate(self, source, **kwargs):

        m=self.getModel(source, **kwargs)
        if m: return self.getView(m, **kwargs)

    def handleOpen(self, source, **kwargs):

        v=self.handleInitiate(source, **kwargs)
        if v: self.activateView(v, **kwargs)
        return v

    def getConfig(self, obj):

        c=self.app.config
        conf={}
        for i in obj.__mro__[::-1]:
            n=i.__name__
            conf.update(c.get(n, {}))
        conf.update(c.get(obj.name, {}))
        return conf
