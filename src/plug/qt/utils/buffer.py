from PyQt5 import QtCore

class Buffer(QtCore.QObject):

    viewCreated=QtCore.pyqtSignal(object)
    modelLoaded=QtCore.pyqtSignal(object)
    modelCreated=QtCore.pyqtSignal(object)

    def __init__(self):

        self.m_views=[]
        self.m_models={}
        self.m_cview=None
        self.m_pview=None
        self.m_cmodel=None
        self.m_pmodel=None
        super().__init__()

    def getModel(self, idx):
        return self.m_models.get(idx, None)

    def setModel(self, idx, m):

        if not m: return
        c, p = m, self.m_pmodel
        self.m_cmodel, self.m_pmodel=c, p
        self.m_models[idx]=m
        self.modelCreated.emit(m)
        if hasattr(m, 'loaded'):
            m.loaded.connect(self.modelLoaded)

    def getCurrentModel(self):

        return self.m_models.get(
                self.m_cmodel, None)

    def getView(self, m):

        for v in self.m_views:
            if v.model()==m:
                return v

    def setView(self, model, view):

        if view: 
            c, p = model, self.m_pview
            self.m_cview, self.m_pview=c, p
            self.m_views+=[view]
            self.viewCreated.emit(view)

    def getCurrentView(self):

        return self.m_views.get(
                self.m_cview, None)
