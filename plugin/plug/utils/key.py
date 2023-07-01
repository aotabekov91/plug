import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher

from pyqtkeybind import keybinder

class OSListener(QAbstractNativeEventFilter):

    def __init__(self, app):

        super().__init__()

        self.shortcuts=[]
        self.app_id=id(app)
        keybinder.init()
        self.setup()

    def setup(self):

        event_dispatcher = QAbstractEventDispatcher.instance()
        event_dispatcher.installNativeEventFilter(self)

    def listen(self, key, func):

        self.shortcuts+=[key]
        keybinder.register_hotkey(self.app_id, key, func)

    def unlisten(self, key):

        keybinder.unregister_hotkey(self.app_id, key)

    def unlistenAll(self):

        for key in self.shortcuts: self.unlisten(key)

    def nativeEventFilter(self, eventType, message):

        return keybinder.handler(eventType, message), 0

if __name__ == '__main__':

    def callback(): print("hello world")

    def exit_app(window): window.close()

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    os_listener = OSListener(app)
    os_listener.listen("Shift+Ctrl+A", callback)
    os_listener.listen("Shift+Ctrl+E", lambda: exit_app(window))

    window.show()
    app.exec_()

    os_listener.unlistenAll()
