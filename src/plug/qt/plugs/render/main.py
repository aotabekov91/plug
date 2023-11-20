import re
from plug.qt import Plug

class Render(Plug):

    kind=None
    view=None
    pattern=None
    view_class=None
    model_class=None

    def type(self):

        if self.kind:
            return self.kind
        elif self.view:
            return self.view.model().kind
        else:
            return self.__class__.__name__

    def setup(self):

        super().setup()
        self.app.handlers.append(self)

    def open(self, source, **kwargs):

        model=self.getModel(source, **kwargs)
        view=self.getView(model, **kwargs)
        self.setView(view, **kwargs)

    def getModel(self, source, **kwargs):

        m=self.app.buffer.getModel(source)
        c=[not m, source, self.model_class]
        if all(c):
            m=self.model_class(
                    render=self,
                    source=source, 
                    **kwargs
                    )
            self.app.buffer.setModel(source, m)
        return m

    def getView(self, model, **kwargs):

        config=self.getConfig()
        v=self.app.buffer.getView(model)
        if not v or not self.unique:
            v=self.view_class(
                    render=self,
                    config=config, 
                    **kwargs)
            v.setModel(model)
            self.app.uiman.setUI(self, v)
            self.app.buffer.setView(model, v)
        return v

    def getConfig(self):

        c=self.app.config
        g=c.get('View', {})
        v=self.view_class
        s=c.get(v.__name__, {})
        for k, v in g.items():
            if not k in s: s[k]=v
            sv=s[k]
            if type(sv)==dict:
                v.update(sv)
                s[k]=v
        return s

    def setupView(self, view):

        self.app.uiman.setUI(self, view)
        self.view=view

    def setView(self, view, **kwargs):

        self.focusView(view)
        self.app.uiman.activate(self, **kwargs)

    def focusView(self, view):

        self.view=view
        m=self.app.moder
        m.viewWanted.emit(view)

    def isCompatible(self, source):

        if source and self.pattern:
            return re.match(
                    self.pattern, 
                    source, 
                    re.I)
