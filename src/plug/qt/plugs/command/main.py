from plug.qt import Plug

class Command(Plug):

    client=None
    name='command'
    listen_leader='<c-,>'
    delisten_on_exec=True

    def setup(self):

        super().setup()
        self.app.moder.modeIsToBeSet.connect(
                self.setClient)

    def setClient(self, mode):

        if mode==self:
            self.client=self.app.moder.prev
