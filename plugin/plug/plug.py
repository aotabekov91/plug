import os
import zmq
import ast
import inspect
from pathlib import Path

# from configparser import RawConfigParser
from configparser import ConfigParser

class Plug:

    def __init__(self, name=None, config=None, port=None, argv=None):

        if argv!=None:
            super(Plug, self).__init__(argv)
        else:
            super(Plug, self).__init__()

        self.name=name
        self.port=port
        self.config=config

        self.running = False
        self.activated=False

        self.setName()
        self.setConfig()
        self.setSettings()
        self.setConnection()

    def createConfig(self, config_folder=None):

        if not config_folder: 
            folder_name=self.__class__.__name__.lower()
            config_folder=f'~/{folder_name}'

        config_folder=os.path.expanduser(config_folder)
        self.config_folder=Path(config_folder)

        if not os.path.exists(config_folder): 
            self.config_folder.mkdir(parents=True, exist_ok=True)

    def handle(self, request):

        print(f'{self.__class__.__name__} received: {request}')

    def readConfig(self): 

        file_path=os.path.abspath(inspect.getfile(self.__class__))
        folder_path=os.path.dirname(file_path).replace('\\', '/')
        config_path=f'{folder_path}/config.ini'
        config=ConfigParser()
        config.optionxform=str
        config.read(config_path)
        return config

    def setName(self):

        if self.name is None: self.name=self.__class__.__name__.lower()

    def setConfig(self):

        if self.config is None: self.config=self.readConfig()

    def setSettings(self):

        if self.config.has_section('Settings'):
            config=dict(self.config['Settings'])
            for name, value in config.items():
                try:
                    value=ast.literal_eval(value)
                except:
                    pass
                attr=getattr(self, name, None)
                if not attr:
                    setattr(self, name, value)

    def setListener(self, kind=zmq.PULL):

        if self.port:
            self.socket = zmq.Context().socket(kind)
            self.socket.bind(f'tcp://*:{self.port}')

    def setConnection(self):

        if self.port:
            try:
                self.setListener()
            except:
                self.socket=None
                print(f'{self.port} is busy')

    def run(self):

        self.running=True
        while self.running and self.socket:
            request=self.socket.recv_json()
            answer=self.handle(request)
            if answer: self.socket.send_json(answer)

    def exit(self):

        self.running=False
        self.os_listener.unlistenAll()
