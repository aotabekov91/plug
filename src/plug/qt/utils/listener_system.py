from PyQt5.QtCore import QObject
from plug.utils.listener_system import SystemListener as Base

class SystemListener(Base, QObject): 
    pass
