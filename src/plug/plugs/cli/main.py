from argparse import ArgumentParser

from plug import Plug
from plug.plugs.connect import Connect

class CLI(Plug):

    def __init__(self, *args, **kwargs):

        self.connect=None
        self.handler_port=None
        super(CLI, self).__init__(
                *args, **kwargs)

    def setup(self):

        super().setup()
        self.setParser()
        self.setConnection()

    def setParser(self):

        self.parser=ArgumentParser()
        self.parser.add_argument('command')
        self.parser.add_argument('-p', '--part')

    def setConnection(self): 

        if self.handler_port:
            self.connect=Connect(
                    parent_port=self.handler_port)
            self.connect.set(parent_kind='PUSH')

    def modeAction(self, 
                   mode=None, 
                   action=None, 
                   request={}):

        request['part']=mode
        request['action']=action
        self.connect.send(request)

    def run(self):

        a, u = self.parser.parse_known_args()
        request={}
        for i in range(0, len(u), 2):
            request[u[i][2:]]=u[i+1]
        if a.command:
            self.modeAction(
                    a.part, a.command, request)

def run():

   app=CLI()
   app.run()
