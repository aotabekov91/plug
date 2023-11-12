from PyQt5 import QtCore

class Buffer(QtCore.QObject):

    viewCreated=QtCore.pyqtSignal(object)
    modelCreated=QtCore.pyqtSignal(object)

    def __init__(self):

        self.views=[]
        self.models={}
        self.m_cview=None
        self.m_pview=None
        self.m_cmodel=None
        self.m_pmodel=None
        super().__init__()

    def getModel(self, idx):

        if idx in self.models:
            return self.models[idx]

    def setModel(self, idx, model):

        if model: 
            c, p = idx, self.m_pmodel
            self.m_cmodel, self.m_pmodel=c, p
            self.models[idx]=model
            self.modelCreated.emit(model)

    def getCurrentModel(self):

        return self.models.get(
                self.m_cmodel, None)

    def getView(self, model):

        for v in self.views:
            if v.model()==model:
                return v

    def setView(self, model, view):

        if view: 
            c, p = model, self.m_pview
            self.m_cview, self.m_pview=c, p
            self.views+=[view]
            self.viewCreated.emit(view)

    def getCurrentView(self):

        return self.views.get(
                self.m_cview, None)
