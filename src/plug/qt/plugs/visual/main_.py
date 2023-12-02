from plug.qt import Plug

class Visual(Plug):

    isMode=True 
    name='visual' 
    listen_leader='v'

    def checkLeader(self, e, p):

        v=self.app.handler.view()
        m=self.app.handler.mode()
        c=m.name in ['normal', 'visual']
        if c and self.checkProp('canSelect', v):
            self.view=v
            return True
