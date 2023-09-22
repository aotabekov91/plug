from PyQt5.QtCore import QObject
from plug.utils.listener_key import KeyListener as Base

class KeyListener(Base, QObject): 
    pass
