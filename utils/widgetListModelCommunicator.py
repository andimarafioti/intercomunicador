from PySide.QtCore import QObject, Signal

__author__ = 'Dev6'


class WidgetListModelCommunicator(QObject):
    ExecuteQueryFinish = Signal(object)