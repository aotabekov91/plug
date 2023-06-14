import os
import sys
import inspect
import argparse
import configparser

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..manager import Manager
from ..window import StackWindow

class BaseApp(QApplication):

    actionRegistered=pyqtSignal()

    def __init__(self):

        super().__init__([])

        self.setConfig()

        self.manager=Manager(self)
        self.stack=StackWindow(self)

        self.initiate()

    def initiate(self):

        self.loadPlugins()
        self.loadModes()
        self.parse()

    def loadPlugins(self): self.plugins.load()

    def loadModes(self): self.modes.load()

    def setConfig(self):

        file_path=os.path.abspath(inspect.getfile(self.__class__))
        mode_path=os.path.dirname(file_path).replace('\\', '/')
        self.configPath=f'{mode_path}/config.ini'
        self.config=configparser.RawConfigParser()
        self.config.optionxform=str
        self.config.read(self.configPath)

    def parse(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('file', nargs='?', default=None, type=str)
        parsed_args, unparsed_args = parser.parse_known_args()
        self.main.open(filePath=parsed_args.file)

if __name__ == "__main__":
    app = BaseApp()
    sys.exit(app.exec_())
