import shlex
import argparse
from plug import Plug

class Parser(Plug):

    def __init__(self,
                 *args, app=None, **kwargs):

        self.app=app
        super().__init__(*args, **kwargs)

    def setup(self):

        super().setup()
        self.setParser()

    def addArgument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def setParser(self): 

        self.parser = argparse.ArgumentParser(
                exit_on_error=False)

    def parse(self, text=None): 

        if text:
            text=shlex.split(text)
            return self.parser.parse_known_args(
                    text)
        return self.parser.parse_known_args()
