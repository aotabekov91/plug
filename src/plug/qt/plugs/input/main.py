from plug.qt import Plug
from gizmo.utils import tag

class Input(Plug):

    name='input'
    isMode=True
    listen_leader='<c-i>'

    def activate(self):

        super().activate()
        self.app.earman.setPassive(True)

    def octivate(self):

        super().octivate()
        self.app.earman.setPassive(False)
