# -*- coding: utf-8 -*-
import abc

from PySide.QtCore import QEvent
from PySide.QtGui import QListView, QApplication, QAbstractItemView, QWheelEvent

from gui.utils.widgetListModel import WidgetListModel
from helpers.observer import Subject


class WidgetListView(QListView):
    EVENT_LOADING = 0
    EVENT_DONE_LOADING = 1
    ROWCOUNT_CHANGED = 2

    def __init__(self, parent):
        super(WidgetListView, self).__init__(parent)

        self.subject = Subject(self)

        self.setMouseTracking(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border:0px")
        self.verticalScrollBar().setSingleStep(5)
        self.setVerticalScrollMode(
            QAbstractItemView.ScrollPerPixel)  # Qt Bug: https://bugreports.qt.io/browse/QTBUG-7232
        self.verticalScrollBar().installEventFilter(self)  # Workaround for Qt Bug
        self.setSpacing(16)
        self.setViewMode(QListView.IconMode)
        self.setFlow(QListView.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(QListView.Adjust)
        self.model = WidgetListModel(self)
        self.model.subject.addObserver(self)
        self.setModel(self.model)

    def initialize(self):
        query_string, params = self.getQuery()
        self.model.updateQuery(query_string, params)

    # Workaround para scrollear de a poco con la rueda del mouse:
    def eventFilter(self, obj, event):
        if obj == self.verticalScrollBar():
            if event.type() == QEvent.Wheel:
                new_event = QWheelEvent(event.pos(), event.globalPos(), 10 * (event.delta() / abs(event.delta())),
                                        event.buttons(), event.modifiers(), event.orientation())
                self.verticalScrollBar().removeEventFilter(self)
                QApplication.sendEvent(self.verticalScrollBar(), new_event)
                self.verticalScrollBar().installEventFilter(self)
                return True

        return False

    def onNotify(self, emitter, event, args):
        if emitter == self.model:
            if event == emitter.EVENT_LOADING:
                self.subject.notify(self.EVENT_LOADING)
            elif event == emitter.EVENT_DONE_LOADING:
                self.subject.notify(self.EVENT_DONE_LOADING)
            elif event == emitter.ROWCOUNT_CHANGED:
                self.subject.notify(self.ROWCOUNT_CHANGED, args[0])

    @abc.abstractmethod
    def getNewWidget(self, index):
        return


