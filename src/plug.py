import os
import re
import zmq
import ast
import yaml
import inspect
from pathlib import Path
from threading import Thread

from configparser import ConfigParser

class Plug:

    def __init__(self, 
                 name=None, 
                 config=None, 
                 port=None, 
                 parent_port=None,
                 umay_port=None,
                 argv=None):

        if argv!=None:
            super(Plug, self).__init__(argv)
        else:
            super(Plug, self).__init__()

        self.name=name
        self.port=port
        self.config=config
        self.umay_port=umay_port
        self.parent_port=parent_port

        self.intents=None
        self.entities=None
        self.running = False
        self.activated=False

        self.setup()

    def setup(self):

        self.setName()
        self.setConfig()
        self.setSettings()
        self.setConnection()
        self.registerByParent()
        self.registerByUmay()

    def setOSListener(self): pass

    def setOSShortcuts(self):

        if self.config.has_section('OSShortcut'):
            self.setOSListener()
            config=dict(self.config['OSShortcut'])
            for func_name, key in config.items():
                func=getattr(self, func_name, None)
                key=re.sub(r'(Shift|Alt|Ctrl)', r'<\1>', key).lower() 
                if func: self.os_listener.listen(key, func)

    def registerByParent(self):

        if self.parent_port:

            self.parent_socket=zmq.Context().socket(zmq.REQ)
            self.parent_socket.connect(
                    f'tcp://localhost:{self.parent_port}')

            self.parent_socket.send_json({
                'command': 'register',
                'mode': self.__class__.__name__,
                'port': self.port
                })
            respond=self.parent_socket.recv_json()
            print(respond)

    def registerByUmay(self):

        if self.umay_port:

            self.umay_socket=zmq.Context().socket(zmq.PUSH)
            self.umay_socket.connect(
                    f'tcp://localhost:{self.umay_port}')

            self.umay_socket.send_json({
                'action': 'register',
                'mode': self.__class__.__name__,
                'port': self.port,
                'files': [self.intents, self.entities],
                })

    def createConfig(self, config_folder=None):

        if not config_folder: 
            folder_name=self.__class__.__name__.lower()
            config_folder=f'~/{folder_name}'

        config_folder=os.path.expanduser(config_folder)
        self.config_folder=Path(config_folder)

        if not os.path.exists(config_folder): 
            self.config_folder.mkdir(parents=True, exist_ok=True)

    def handle(self, request):

        print(f'{self.name} received: ', request)

        action=request.get('action', None)

        func=None
        if action:

            func=getattr(self, action, None)
            if not func and hasattr(self, 'ui'): 
                func=getattr(self.ui, action, None)

        if func:
            prmts=inspect.signature(func).parameters
            if len(prmts)==0:
                func()
            elif 'request' in prmts:
                func(request)
            else:
                fp={p:request[p] for p in prmts if p in request}
                if fp:
                    func(**fp)
                else:
                    msg=f'{self.__class__.__name__}: not understood'

            msg=f"{self.__class__.__name__}: handled request"

        else:

            msg=f'{self.__class__.__name__}: not understood'

        return msg

    def setName(self):

        if self.name is None: self.name=self.__class__.__name__

    def setConfig(self):

        file_path=os.path.abspath(
                inspect.getfile(self.__class__))
        folder_path=os.path.dirname(
                file_path).replace('\\', '/')

        if self.config is None: 
            self.config_path=f'{folder_path}/config.ini'
            self.config=ConfigParser()
            self.config.optionxform=str
            self.config.read(self.config_path)

        intents=f'{folder_path}/intents.yaml'
        entities=f'{folder_path}/entities.yaml'

        if os.path.exists(intents): 
            with open(intents, 'r') as f:
                self.intents=list(yaml.safe_load_all(f))
        if os.path.exists(entities): 
            with open(entities, 'r') as f:
                self.entities=list(yaml.safe_load_all(f))

    def setSettings(self):

        if self.config.has_section('Settings'):
            config=dict(self.config['Settings'])
            for name, value in config.items():
                try:
                    value=ast.literal_eval(value)
                except:
                    pass
                attr=getattr(self, name, None)
                if not attr: setattr(self, name, value)

    def setConnection(self, kind=zmq.PULL):

        if self.port:
            self.socket = zmq.Context().socket(kind)
            self.socket.bind(f'tcp://*:{self.port}')

    def run(self, answer=False):

        self.running=True
        while self.running and self.socket:
            request=self.socket.recv_json()
            respond=self.handle(request)
            if answer: self.socket.send_json(respond)

    def exit(self): self.running=False

    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    def activate(self):

        if not self.activated:
            self.activated=True
            if hasattr(self, 'ui'):
                self.ui.show()

    def deactivate(self):

        if self.activated:
            self.activated=False
            if hasattr(self, 'ui'):
                self.ui.hide()
