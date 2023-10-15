import zmq
import threading
from plug import Plug

class Connect(Plug):

    def __init__(self, 
                 *args, 
                 port=None,
                 kind=None,
                 handler=None,
                 parent_port=None,
                 **kwargs):

        self.port=port
        self.kind=kind
        self.handler=handler
        self.poller=zmq.Poller()
        self.parent_port=parent_port
        self.socket=kwargs.get('socket', None)
        super().__init__(*args, **kwargs)

    def set(self, 
            kind='PULL', 
            port_kind='PUSH',
            parent_kind='REQ', 
            socket_kind=None,
            ):

        if self.parent_port:
            self.psocket = self.get(
                    parent_kind)
            s=f'tcp://localhost:{self.parent_port}'
            self.psocket.connect(s)
        if socket_kind=='bind':
            self.kind=kind
            self.socket = self.get(kind)
            if self.port:
                socket=f'tcp://*:{self.port}'
                self.socket.bind(socket)
            else: 
                self.port=self.socket.bind_to_random_port(
                        'tcp://*')

    def get(self, kind):

        return zmq.Context().socket(
                getattr(zmq, kind))

    def send(self, 
             data, 
             socket, 
             wait_time=2500,
             pollerize=True, 
            ):

        socket.send_json(data)
        if not pollerize:
            return socket.recv_json()
        else:
            self.poller.register(
                    socket, flags=zmq.POLLIN)
            if self.poller.poll(timeout=wait_time):
                res=socket.recv_json()
            else:
                socket.setsockopt(zmq.LINGER, 1)
                res={'status': 'nok', 
                    'info': 'no response'}
            self.poller.unregister(socket)
            return res

    def stop(self):
        self.running=False

    def run(self):

        def listen():

            while self.running:
                q=self.socket.recv_json()
                a=self.handle(q)
                if a: 
                    self.socket.send_json(a)

        if self.socket:
            self.running=True
            self.thread=threading.Thread(
                    target=listen)
            self.thread.deamon=True
            self.thread.start()
            return self.thread

    def handle(self, r):

        if self.handler:
            return self.handler(r)
