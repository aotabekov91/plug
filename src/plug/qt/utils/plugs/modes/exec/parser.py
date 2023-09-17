import re
import argparse

class ArgumentParser(argparse.ArgumentParser):    

    ptrn1=r"the following arguments[^:]*: *(.*)"
    ptrn2=r".* invalid choice: *'([^']*)'"

    def error(self, message):

        m1=re.match(self.ptrn1, message)
        m2=re.match(self.ptrn2, message)
        if m1:
            arg=m1.group(1)
            command=self.prog.split(' ')[-1]
            raise ValueError(command, arg)
        elif m2:
            arg=m2.group(1)
            raise LookupError(arg)
        else:
            super(ArgumentParser, self).error(message)
