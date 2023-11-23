from plug.qt import Plug

class ModelFactory(Plug):

    def setup(self):

        super().setup()
        self.createFactories()

    def createFactories(self):

        self.m_factories={}
        for f, conf in self.config.items():
            f=TableModelFactory(
                    app=self.app,
                    config=conf)
            self.m_factories[f]=f
