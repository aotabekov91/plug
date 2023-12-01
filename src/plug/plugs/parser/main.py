import shlex
import argparse
from plug import Plug

class Parser(Plug):

    def __init__(self,
                 *args, 
                 app=None, 
                 **kwargs):

        self.app=app
        super().__init__(*args, **kwargs)

    def setup(self):

        super().setup()
        self.setParser()
        self.m_subparsers={}

    def addArgument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def setParser(self): 

        self.parser = argparse.ArgumentParser(
                exit_on_error=False)

    def addSubParser(self, *args, **kwargs):

        return self.parser.add_subparsers(
                *args, **kwargs)

    def split(self, text):
        return shlex.split(text)

    def parse(self, text=None, pref=None, only_known=True): 

        f=self.parser.parse_args
        if only_known:
            f=self.parser.parse_known_args
        if text:
            t=shlex.split(text)
            if pref: t.insert(0, pref)
            return f(t)
        return f()
