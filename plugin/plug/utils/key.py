from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from pynput import keyboard

class OSListener(QObject):

    def __init__(self, parent):

        super(OSListener, self).__init__()

        self.hotkeys=[]
        self.parent = parent

        self.listener=keyboard.Listener(
                on_release=self.on_release,
                on_press=self.on_press)

    def listen(self, key, func): 

        self.hotkeys += [keyboard.HotKey(
                keyboard.HotKey.parse(key), 
                func)]

    def on_release(self, key):

        for hotkey in self.hotkeys:
            hotkey.release(self.listener.canonical(key))

    def on_press(self, key):

        for hotkey in self.hotkeys:
            hotkey.press(self.listener.canonical(key))

    def loop(self): self.listener.start()
