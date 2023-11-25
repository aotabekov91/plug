from PyQt5 import QtCore

class Handler(QtCore.QObject):

    viewAdded=QtCore.pyqtSignal(object)
    typeAdded=QtCore.pyqtSignal(object)
    typerAdded=QtCore.pyqtSignal(object)
    viewWanted=QtCore.pyqtSignal(object)
    modelAdded=QtCore.pyqtSignal(object)
    typeWanted=QtCore.pyqtSignal(object)
    viewChanged=QtCore.pyqtSignal(object)
    typeChanged=QtCore.pyqtSignal(object)
    viewerAdded=QtCore.pyqtSignal(object)
    modellerAdded=QtCore.pyqtSignal(object)

    def __init__(self, app, config):

        super().__init__(app)
        self.app=app
        self.m_type=None
        self.m_view=None
        self.m_typers=[]
        self.m_viewers=[]
        self.m_modellers=[]
        self.m_config=config
        self.uiman=self.app.uiman
        self.buffer=self.app.buffer
        self.setup()

    def setup(self):

        self.setSettings()
        self.typeWanted.connect(
                self.setType)
        self.viewWanted.connect(
                self.setView)

    def setDefault(self):

        v=self.app.display.currentView()
        self.setView(v)

    def setView(self, v):

        self.m_view=v
        if not v: return
        m=v.model()
        if v: v.setFocus()
        if m and m.isType: 
            self.setType(v) 
        self.viewChanged.emit(v)

    def setType(self, v):

        self.m_type=v
        self.typeChanged.emit(v)

    def type(self):
        return self.m_type

    def view(self):
        return self.m_view

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

    def getModel(self, s, **kwargs):

        for k in self.m_modellers:
            if k.isCompatible(s):
                n=k.getSourceName(s, **kwargs)
                m=self.buffer.getModel(n)
                if not m:
                    c=self.getConfig(k)
                    m=k(source=s, config=c, **kwargs)
                    self.buffer.setModel(n, m)
                    m.load()
                return m

    def getView(self, m, **kwargs):

        for k in self.m_viewers:
            if k.isCompatible(m):
                v=self.buffer.getView(m)
                if not v or not m.wantUniqView:
                    c=self.getConfig(k)
                    v=k(config=c, app=self.app, **kwargs)
                    v.setModel(model=m)
                    self.buffer.setView(m, v)
                    self.uiman.setupUI(
                        ui=v, name=v.name)
                    self.viewAdded.emit(v)
                    if m.isType:
                        self.typeAdded.emit(v)
                    v.activateWanted.connect(
                            self.activateView)
                    v.octivateWanted.connect(
                            self.octivateView)
                return v

    def activateView(self, v, **kwargs):

        self.setView(v)
        self.uiman.activate(ui=v, **kwargs)

    def octivateView(self, v, **kwargs):

        self.setDefault()
        self.uiman.octivate(ui=v, **kwargs)

    def handleInitiate(self, source, **kwargs):

        m=self.getModel(source, **kwargs)
        return self.getView(m, **kwargs)

    def handleOpen(self, source, **kwargs):

        v=self.handleInitiate(source, **kwargs)
        self.activateView(v, **kwargs)

    def getConfig(self, obj):

        c=self.app.config
        conf={}
        for i in obj.__mro__[::-1]:
            n=i.__name__
            conf.update(c.get(n, {}))
        conf.update(c.get(obj.name, {}))
        return conf
