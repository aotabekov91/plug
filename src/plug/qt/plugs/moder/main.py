from plug.plugs.moder import Moder as Base
from PyQt5.QtCore import QObject, pyqtSignal

class Moder(Base, QObject):

    plugAdded=pyqtSignal(object)
    plugsLoaded=pyqtSignal(object)
    modeChanged=pyqtSignal(object)
    modeIsToBeSet=pyqtSignal(object)
    actionsRegistered=pyqtSignal(object, object)

    def setup(self):

        super().setup()
        self.app.window.focusGained.connect(
                self.on_focused)
        self.app.appLaunched.connect(
                lambda: self.set(self.default))

    def on_focused(self):
        self.set(self.current)

    def add(self, plug):

        super().add(plug)
        self.plugAdded.emit(plug)

    def load(self, *args, **kwargs):

        super().load(*args, **kwargs)
        self.plugsLoaded.emit(self.plugs)

    def set(self, mode=None):

        m=self.get(mode)
        self.modeIsToBeSet.emit(m)
        m=super().set(m)
        if m: self.modeChanged.emit(m)
        return m

    def save(self, plug, actions):

        super().save(plug, actions)
        self.actionsRegistered.emit(plug, actions)
