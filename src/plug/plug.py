import os
import re
import zmq
import yaml
import tomli
import inspect
import argparse

from pathlib import Path
from types import MethodType, BuiltinFunctionType

from plug.utils import Plugman

class Plug:

    def __init__(self, 
                 name=None, 
                 port=None, 
                 config={}, 
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

        self.files={}
        self.yamls={}
        self.tomls={}
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
        self.setBasePath()
        self.setFiles()
        self.setSettings()
        self.setConnection()
        self.registerByParent()
        self.registerByUmay()
        self.setSystemShortcut()
        self.setActions()

    def setPlugman(self): 
        self.plugman=Plugman(self)

    def setParser(self): 
        self.parser = argparse.ArgumentParser()


    def setSystemShortcut(self):

        if self.config.get('System'):
            self.setSystemListener()
            shortcuts=self.config['System']
            for func_name, key in shortcuts.items():
                func=getattr(self, func_name, None)
                key=re.sub(r'(Shift|Alt|Ctrl)', 
                           r'<\1>', 
                           key).lower() 
                if func: 
                    self.os_listener.listen(key, func)

    def setActions(self, obj=None):

        if self.config.get('Keys'):
            keys=self.config['Keys']
            for f, key in keys.items():
                m=getattr(self, f, None)
                if m and hasattr(m, '__func__'):
                    if type(key)==str:
                        modes=getattr(m, 'modes', ['command'])
                        setattr(m.__func__, 'key', f'{key}')
                    elif 'key' in key:
                        modes=getattr(m, 'modes', ['command'])
                        modes=key.get('modes', modes)
                        key=key.get('key')
                    f=getattr(m, 'name', m.__func__.__name__)
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

    def registerByParent(self, kind='PUSH'):

        def register(kind):

            if self.parent_port:

                self.parent_socket = self.getConnection(kind='REQ')
                self.parent_socket.connect(
                        f'tcp://localhost:{self.parent_port}')

                self.parent_socket.send_json({
                    'command': 'register',
                    'mode': self.__class__.__name__,
                    'port': self.port,
                    'kind': kind,
                    })

                poller=zmq.Poller()
                poller.register(
                        self.parent_socket,
                        flags=zmq.POLLIN)

                if poller.poll(timeout=1000):
                    respond=self.parent_socket.recv_json()
                else:
                    self.parent_socket.setsockopt(zmq.LINGER, 1)
                    respond={'status':'nok',
                             'info': 'No parent response'}
                return respond

        # thread=Thread(target=register, args=[kind])
        # thread.deamon=True
        # thread.start()
        register(kind)

    def register(self, request): pass

    def registerByUmay(self, paths=None, kind='PUSH'):

        def register(paths, kind):

            if self.umay_port and self.listen_port:

                self.umay_socket = self.getConnection(kind='REQ')
                self.umay_socket.connect(
                        f'tcp://localhost:{self.umay_port}')

                if not paths: paths=[self.intents, self.entities]

                self.umay_socket.send_json({
                    'paths': paths, 
                    'port': self.port,
                    'action': 'register',
                    'keyword': self.keyword,
                    'mode': self.__class__.__name__,
                    'kind': kind,
                    })

                poller=zmq.Poller()
                poller.register(
                        self.umay_socket,
                        flags=zmq.POLLIN)

                if poller.poll(timeout=1000):
                    respond=self.umay_socket.recv_json()
                else:
                    self.umay_socket.setsockopt(zmq.LINGER, 1)
                    respond={'status':'nok',
                             'info': 'No umay response'}
                return respond

        # thread=Thread(target=register, args=[paths, kind])
        # thread.deamon=True
        # thread.start()
        register(paths, kind)

    def createFolder(self, folder=None, attr_name='folder'):

        if not folder: 
            name=self.__class__.__name__.lower()
            folder=f'~/{name}'

        folder=os.path.expanduser(folder)

        attr=Path(folder)
        setattr(self, attr_name, attr)

        if not os.path.exists(folder): 
            attr.mkdir(parents=True, exist_ok=True)

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

    def setBasePath(self):

        file_path=os.path.abspath(
                inspect.getfile(self.__class__))
        self.path=os.path.dirname(
                file_path).replace('\\', '/')

    def setFiles(self):

        for f in os.listdir(self.path):

            name=f.rsplit('.', 1)[0]
            path=f'{self.path}/{f}'

            self.files[f]=path

            if f.endswith('yaml'):
                with open(path, 'r') as y:
                    if f=='config.yaml':
                        l=yaml.loader.SafeLoader
                        config=yaml.load(y, Loader=l)
                        config.update(self.config)
                        self.config=config
                    else:
                        self.yamls[name]=list(
                                yaml.safe_load_all(f))
            elif f.endswith('toml'):
                with open(path, 'rb') as y:
                    toml_data=tomli.load(y)
                    self.tomls[name]=toml_data
                    if f=='config.toml':
                        toml_data.update(self.config)
                        self.config=toml_data

    def setSettings(self):

        if self.config.get('Settings', None):
            settings=self.config['Settings']
            for name, value in settings.items():
                setattr(self, name, value)

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

        self.activated=True
        if hasattr(self, 'ui'): self.ui.show()

    def deactivate(self):

        self.activated=False
        if hasattr(self, 'ui'): self.ui.hide()
