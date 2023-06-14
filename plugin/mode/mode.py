import os
import sys
import zmq
import time
import inspect

from os.path import abspath
from configparser import ConfigParser

from ..plug import AppPlug

class Mode(AppPlug):

    def __init__(self, 
                 name=None, 
                 port=None, 
                 parent_port=None, 
                 config=None,
                 window_classes='all',
                 app_name='own_floating',
                 leader=None,
                 ):

        self.parent_port=parent_port
        self.window_classes=window_classes

        super(Mode, self).__init__(name=name, port=port, config=config, leader=leader,  app_name=app_name)

        self.register()

    def get_mode_folder(self):
        file_path=os.path.abspath(inspect.getfile(self.__class__))
        return os.path.dirname(file_path).replace('\\', '/')

    def register(self):
        if self.parent_port:
            poller=zmq.Poller()
            poller.register(self.parent_socket, flags=zmq.POLLIN)
            self.parent_socket.send_json({
                'command': 'registerMode',
                'mode_name':self.__class__.__name__,
                'keyword':self.name,
                'port': self.port,
                'window_classes': self.window_classes})
            sock=poller.poll(timeout=1000)
            if len(sock)>0 and sock[0][0]==self.parent_socket:
                respond=self.parent_socket.recv_json(zmq.NOBLOCK)
            poller.unregister(self.parent_socket)

    def handle(self, request):
        print(f'{self.__class__.__name__} received: {request}')
        command=request['command'].rsplit('_', 1)
        mode_name, action=command[0], command[-1]
        mode_func=getattr(self, action, False)
        if not mode_func and hasattr(self, 'ui'):
            mode_func=getattr(self.ui, action, None)
        # try:

        if mode_func:
            if 'request' in inspect.signature(mode_func).parameters:
                mode_func(request)
            else:
                mode_func()
            msg=f"{self.__class__.__name__}: handled request"
        elif not mode_name in [self.__class__.__name__, 'CurrentMode']:
            if self.parent_port:
                self.parent_socket.send_json(
                        {'command':'setModeAction',
                         'mode_name':mode_name,
                         'mode_action': request['command'],
                         'slot_names': request['slot_names'],
                         'intent_data': request['intent_data'],
                         'own_only': True})
                respond=self.parent_socket.recv_json()
                msg=f'{self.__class__.__name__}: {mode_name} {request["command"]}'
            else:
                msg=f'{self.__class__.__name__}: {mode_name} no parent to redirect'
        else:
            msg=f'{self.__class__.__name__}: not understood'

    def setConnection(self):
        socket=super().setConnection(exit=False)
        if self.parent_port:
            self.parent_socket=zmq.Context().socket(zmq.REQ)
            self.parent_socket.connect(f'tcp://localhost:{self.parent_port}')
        if socket:
            socket.send_json({'command':'setParentPort', 'parent_port':self.parent_port})
            sys.exit()

    def setParentPort(self, request):
        self.parent_port=request['parent_port']
        self.register()

if __name__=='__main__':
    app=Mode(port=33333, parent_port=44444)
    app.run()
