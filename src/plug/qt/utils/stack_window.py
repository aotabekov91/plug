from PyQt5.QtCore import pyqtSignal
from gizmo.ui import StackWindow as Base

class StackWindow(Base):

    viewItemChanged=pyqtSignal(
            object, object)
    viewIndexChanged=pyqtSignal(
            object, object)
    viewItemPainted=pyqtSignal(
            object, object, object)
    viewPositionChanged=pyqtSignal(
            object, object)
    viewMouseMoveOccured=pyqtSignal(
            object, object)
    viewHoverMoveOccured=pyqtSignal(
            object, object)
    viewMousePressOccured=pyqtSignal(
            object, object)
    viewMouseReleaseOccured=pyqtSignal(
            object, object)
    viewMouseDoubleClickOccured=pyqtSignal(
            object, object)
    viewItemPositionChanged=pyqtSignal(
            object, object, object)
    viewItemMouseMoveOccured=pyqtSignal(
            object, object, object)
    viewItemHoverMoveOccured=pyqtSignal(
            object, object, object)
    viewItemMousePressOccured=pyqtSignal(
            object, object, object)
    viewItemMouseReleaseOccured=pyqtSignal(
            object, object, object)
    viewItemMouseDoubleClickOccured=pyqtSignal(
            object, object, object)
