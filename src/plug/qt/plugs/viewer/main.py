from plug.qt import Plug

class Viewer(Plug):

    position=None
    view_class=None
    model_class=None

    def initiate(self, *args, **kwargs):

        super().initiate(*args, **kwargs)
        self.app.addRender(self)

    def open(self, source=None, **kwargs):

        model=self.getModel(
                source, **kwargs)
        view=self.getView(
                model, **kwargs)
        self.setView(view, **kwargs)

    def getModel(self, source, **kwargs):

        m=self.app.buffer.getModel(source)
        c=[not m, source, self.model_class]
        if all(c):
            m=self.model_class(
                    source=source, **kwargs)
            self.app.buffer.setModel(source, m)
        return m

    def getView(self, model, **kwargs):

        config=self.getConfig()
        v=self.app.buffer.getView(model)
        if not self.unique or not v:
            v=self.view_class(
                    app=self.app, 
                    config=config, 
                    **kwargs)
            v.setModel(model)
            self.app.buffer.setView(model, v)
        return v

    def isCompatible(self, s):
        return self.model_class.isCompatible(s)

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

    def setView(self, view, **kwargs):

        if self.position=='display':
            self.app.display.setupView(
                    view, **kwargs)
