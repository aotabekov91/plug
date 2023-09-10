import zmq
import threading
from plug import Plug

class Connect(Plug):

    def __init__(self, 
                 *args, 
                 app=None,
                 port=None,
                 handler=None,
                 parent_port=None,
                 **kwargs):

        self.app=app
        self.port=port
        self.handler=handler
        self.parent_port=parent_port
        super().__init__(*args, **kwargs)

    def set(self, 
            kind='PULL', 
            port_kind='PUSH',
            parent_kind='REQ', 
            ):

        self.socket = self.get(kind)
        if self.port:
            socket=f'tcp://*:{self.port}'
            self.socket.bind(socket)
        else: 
            self.port=self.socket.bind_to_random_port(
                    'tcp://*')
        if self.parent_port:
            self.psocket = self.get(parent_kind)
            s=f'tcp://localhost:{self.parent_port}'
            self.psocket.connect(s)

    def get(self, kind):

        return zmq.Context().socket(
                getattr(zmq, kind))

    def send(self, data):

        poller=zmq.Poller()
        poller.register(self.psocket, 
                        flags=zmq.POLLIN)
        for d in data:
            self.psocket.send_json(d)
            if poller.poll(timeout=1000):
                self.psocket.recv_json()
            else:
                self.psocket.setsockopt(
                        zmq.LINGER, 1)

    def run(self):

        self.running=True
        thread=threading.Thread(
                target=self.listen)
        thread.run()

    def listen(self):

        while self.running:
            q=self.socket.recv_json()
            a=self.handle(q)
            if a: 
                self.socket.send_json(a)

    def handle(self, r):

        if self.handler:
            return self.handler(r)
