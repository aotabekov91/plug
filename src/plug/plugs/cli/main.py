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
        self.setConnect()
        self.setHandlerConnect()

    def setParser(self):

        self.parser=ArgumentParser()
        self.parser.add_argument('command')

    def setConnect(self, connect=Connect): 
        self.connect=connect()

    def setHandlerConnect(self):

        if self.handler_port:
            self.socket=self.connect.get('PUSH')
            self.socket.connect(
                    f'tcp://localhost:{self.handler_port}')

    def act(self, action, request={}):

        cmd={action: request}
        self.socket.send_json(cmd)

    def run(self):

        a, u = self.parser.parse_known_args()
        request={}
        for i in range(0, len(u), 2):
            request[u[i][2:]]=u[i+1]
        if a.command:
            self.act(a.command, request)

def run():

   app=CLI()
   app.run()
