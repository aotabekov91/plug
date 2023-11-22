from PyQt5 import QtCore

class Buffer(QtCore.QObject):

    viewCreated=QtCore.pyqtSignal(object)
    modelCreated=QtCore.pyqtSignal(object)

    def __init__(self):

        self.m_view=[]
        self.m_models={}
        self.m_cview=None
        self.m_pview=None
        self.m_cmodel=None
        self.m_pmodel=None
        super().__init__()

    def getModel(self, idx):
        return self.m_models.get(idx, None)

    def setModel(self, idx, model):

        if model: 
            c, p = model, self.m_pmodel
            self.m_cmodel, self.m_pmodel=c, p
            self.m_models[idx]=model
            self.modelCreated.emit(model)

    def getCurrentModel(self):

        return self.m_models.get(
                self.m_cmodel, None)

    def getView(self, model):

        for v in self.m_view:
            if id(v.model())==id(model):
                return v

    def setView(self, model, view):

        if view: 
            c, p = model, self.m_pview
            self.m_cview, self.m_pview=c, p
            self.m_view+=[view]
            self.viewCreated.emit(view)

    def getCurrentView(self):

        return self.m_view.get(
                self.m_cview, None)
