class Copy:

    canCopy=True

    def copy(self):

        c=self.__class__(
                app=self.app, 
                name=self.name, 
                index=self.m_id, 
                config=self.m_config)
        c.setModel(self.m_model)
        self.app.handler.connectView(c)
        idx=self.currentIndex()
        c.setCurrentIndex(idx)
        return c
