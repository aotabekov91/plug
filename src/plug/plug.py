import os
import re
import zmq
import ast
import yaml
import inspect
import argparse
from pathlib import Path

from configparser import ConfigParser

class Plug:

    def __init__(self, 
                 name=None, 
                 port=None, 
                 config=None, 
                 keyword=None,
                 umay_port=19999,
                 parent_port=None,
                 listen_port=True,
                 argv=None,
                 **kwargs,
                 ):

        if argv!=None: 
            super(Plug, self).__init__(argv)
        else:
            super(Plug, self).__init__()

        self.name=name
        self.port=port
        self.config=config
        self.keyword=keyword
        self.umay_port=umay_port
        self.listen_port=listen_port
        self.parent_port=parent_port

        self.socket=None
        self.intents=None
        self.entities=None
        self.running = False
        self.activated=False

        self.setup()

    def setup(self):

        self.setName()
        self.setConfig()
        self.setParser()
        self.setSettings()
        self.setConnection()
        self.registerByParent()
        self.registerByUmay()
        self.setOSShortcuts()

    def setParser(self): self.parser = argparse.ArgumentParser()

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

        if self.umay_port and self.listen_port:

            self.umay_socket=zmq.Context().socket(zmq.PUSH)
            self.umay_socket.connect(
                    f'tcp://localhost:{self.umay_port}')

            paths=[self.intents, self.entities]

            self.umay_socket.send_json({
                'paths': paths, 
                'port': self.port,
                'action': 'register',
                'keyword': self.keyword,
                'mode': self.__class__.__name__,
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
        result=None

        status='nok'

        if action:

            func=getattr(self, action, None)
            if not func and hasattr(self, 'ui'): 
                func=getattr(self.ui, action, None)

        if func:
            prmts=inspect.signature(func).parameters
            if len(prmts)==0:
                result=func()
            elif 'request' in prmts:
                result=func(request)
            else:
                fp={p:request[p] for p in prmts if p in request}
                result=func(**fp)

            status='ok'

        return {'result': result, 'status': status}

    def setName(self):

        if self.name is None: 
            self.name=self.__class__.__name__
        if self.keyword is None:
            self.keyword=self.name.lower()

    def setConfig(self):

        file_path=os.path.abspath(
                inspect.getfile(self.__class__))
        self.path=os.path.dirname(
                file_path).replace('\\', '/')

        self.config_path=f'{self.path}/config.ini'
        self.config=ConfigParser()
        self.config.optionxform=str
        self.config.read(self.config_path)

        intents=f'{self.path}/intents.yaml'
        entities=f'{self.path}/entities.yaml'

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

        if self.port or self.listen_port:
            self.socket = zmq.Context().socket(kind)
            if self.port:
                self.socket.bind(f'tcp://*:{self.port}')
            else: 
                self.port=self.socket.bind_to_random_port(
                        'tcp://*')

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
