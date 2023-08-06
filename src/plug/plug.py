import os
import re
import zmq
import ast
import yaml
import inspect
import argparse

from pathlib import Path
from configparser import ConfigParser
from types import MethodType, BuiltinFunctionType

class Plug:

    def __init__(self, 
                 name=None, 
                 port=None, 
                 config=None, 
                 keyword=None,
                 umay_port=19999,
                 parent_port=None,
                 listen_port=True,
                 respond_port=False,
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
        self.parent_port=parent_port

        self.listen_port=listen_port
        self.respond_port=respond_port

        self.actions={}
        self.commandKeys={}

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
        self.setActions()

    def setParser(self): 

        self.parser = argparse.ArgumentParser()

    def setOSListener(self): pass

    def setOSShortcuts(self):

        if self.config.has_section('OSShortcut'):
            self.setOSListener()
            config=dict(self.config['OSShortcut'])
            for func_name, key in config.items():
                func=getattr(self, func_name, None)
                key=re.sub(r'(Shift|Alt|Ctrl)', r'<\1>', key).lower() 
                if func: 
                    self.os_listener.listen(key, func)

    def setActions(self, obj=None):

        if self.config.has_section('Keys'):
            config=dict(self.config['Keys'])
            for f, key in config.items():
                m=getattr(self, f, None)
                if m and hasattr(m, '__func__'):
                    setattr(m.__func__, 'key', f'{key}')
                    f=getattr(m, 'name', m.__func__.__name__)
                    modes=getattr(m, 'modes', ['command'])
                    setattr(m.__func__, 'name', f)
                    setattr(m.__func__, 'modes', modes)
                    d=(self.__class__.__name__, m.name)
                    self.actions[d]=m 
                    self.commandKeys[m.key]=m

        if not obj: obj=self

        cnd=[MethodType, BuiltinFunctionType]
        for f in obj.__dir__():
            m=getattr(obj, f)
            if type(m) in cnd and hasattr(m, 'modes'):
                name=getattr(obj, 'name', obj.__class__.__name__)
                d=(name, m.name)
                if not d in self.actions:
                    self.actions[d]=m 
                    if type(m.key)==str:
                        self.commandKeys[m.key]=m
                    elif type(m.key)==list:
                        for k in m.key: 
                            self.commandKeys[k]=m

    def registerByParent(self):

        if self.parent_port:

            self.parent_socket = self.getConnection(kind='REQ')
            self.parent_socket.connect(
                    f'tcp://localhost:{self.parent_port}')

            self.parent_socket.send_json({
                'command': 'register',
                'mode': self.__class__.__name__,
                'port': self.port
                })

            poller=zmq.Poller()
            poller.register(
                    self.parent_socket,
                    flags=zmq.POLLIN)

            if poller.poll(timeout=2000):
                respond=self.parent_socket.recv_json()
            else:
                self.parent_socket.setsockopt(zmq.LINGER, 1)
                respond={'status':'nok',
                         'info': 'No parent response'}
            print(respond)
            return respond

    def register(self, request): pass

    def registerByUmay(self):

        if self.umay_port and self.listen_port:

            self.umay_socket = self.getConnection(kind='REQ')
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

            poller=zmq.Poller()
            poller.register(
                    self.umay_socket,
                    flags=zmq.POLLIN)

            if poller.poll(timeout=2000):
                respond=self.umay_socket.recv_json()
            else:
                self.umay_socket.setsockopt(zmq.LINGER, 1)
                respond={'status':'nok',
                         'info': 'No umay response'}
            print(respond)
            return respond

    def createConfig(self, config_folder=None):

        if not config_folder: 
            folder_name=self.__class__.__name__.lower()
            config_folder=f'~/{folder_name}'

        config_folder=os.path.expanduser(config_folder)
        self.config_folder=Path(config_folder)

        if not os.path.exists(config_folder): 
            self.config_folder.mkdir(
                    parents=True, 
                    exist_ok=True)

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
                if action=='quit' and self.respond_port:
                    msg={'status':'ok', 'info':'quitting'}
                    self.socket.send_json(msg)
                    func()
                else:
                    result=func()
            elif 'request' in prmts:
                result=func(request)
            else:
                fp={}
                for p in prmts:
                    if p in request: fp[p]=request[p] 
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

    def getConnection(self, kind):

        kind=getattr(zmq, kind)
        socket=zmq.Context().socket(kind)
        return socket

    def setConnection(self, kind='PULL'):

        if self.port or self.listen_port:
            self.socket = self.getConnection(kind)
            if self.port:
                self.socket.bind(f'tcp://*:{self.port}')
            else: 
                self.port=self.socket.bind_to_random_port(
                        'tcp://*')

    def run(self):

        self.running=True
        while self.running and self.socket:
            request=self.socket.recv_json()
            respond=self.handle(request)
            if self.respond_port: 
                self.socket.send_json(respond)

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
