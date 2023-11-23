from PyQt5.QtCore import QObject

class Handler(QObject):

    def __init__(self, app, config):

        super().__init__(app)
        self.app=app
        self.m_viewers=[]
        self.m_modellers=[]
        self.m_config=config
        self.uiman=self.app.uiman
        self.buffer=self.app.buffer
        self.setSettings()
        self.setup()

    def setSettings(self):

        s=self.m_config.get('Settings', {})
        for n, v in s.items():
            setattr(self, n, v)

    def addView(self, view):
        self.m_viewers+=[view]

    def addModel(self, model):
        self.m_modellers+=[model]

    def getModel(self, source, **kwargs):

        for i in self.m_modellers:
            if i.isCompatible(source):
                m=self.buffer.getModel(source)
                if not m:
                    m=i(source=source, **kwargs)
                    self.buffer.setModel(
                            source, m)
                    m.load()
                return m

    def getView(self, model, **kwargs):

        for i in self.m_viewers:
            if i.isCompatible(model):
                v=self.buffer.getView(model)
                if not v or not v.isUnique:
                    v=i(**kwargs)
                    v.setModel(model=model)
                    self.buffer.setView(model, v)
                    self.uiman.setupUI(
                        ui=v, name=v.name)
                return v

    def handleOpen(self, source, **kwargs):

        m=self.getModel(source, **kwargs)
        v=self.getView(m, **kwargs)
        self.uiman.activate(ui=v, **kwargs)

    def setup(self):
        pass
