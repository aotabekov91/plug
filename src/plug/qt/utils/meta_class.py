from PyQt5 import QtCore

class SetKeys(type(QtCore.QObject)):

    def __call__(cls, *args, **kwargs):

        def setListener(obj, listener):
            pass


        obj=type.__call__(cls, *args, **kwargs)
        obj.setListener=setListener
        return obj
