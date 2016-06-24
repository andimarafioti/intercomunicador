import abc
from threading import Event

from PySide.QtCore import Qt, Signal, QObject
from PySide.QtGui import QWidget, QApplication

from Shiboken import shiboken

from gui.centrals.loadingWidget.loadableWidget import LoadableWidget
from gui.utils.standardLayout import StandardLayout
from helpers.observer import Subject
from helpers.worker.worker import Worker

__author__ = 'Dev6'


class WidgetBoardCommunicator(QObject):
	AddWidgetsFor = Signal(object)
	FillBoard = Signal()


class WidgetBoard(QWidget):
	WIDGETS_PER_BATCH = 20  # This value van be changed is subclasses

	def __init__(self, parent, layoutClass=StandardLayout):
		super(WidgetBoard, self).__init__(parent)
		self.setAttribute(Qt.WA_DeleteOnClose)

		self.items = None
		self.itemCount = 0
		self.noMoreItemsToDisplay = False

		self.subject = Subject(self)

		self._layoutClass = layoutClass

		self.initializeLayout()

		self.communicator = WidgetBoardCommunicator()
		self.communicator.AddWidgetsFor.connect(self.addWidgetsFor, Qt.QueuedConnection)
		self.communicator.FillBoard.connect(self.loadWidgetsUntilScreenIsExceeded, Qt.QueuedConnection)

		self.isAddingWidgets = False

		self._loadWidgetBatchEvent = Event()
		self.widgetLoader = Worker.call(self._widgetLoaderRoutine).asDaemon

	def initialize(self):
		self.subject.notify(LoadableWidget.EVENT_LOADING)
		self.widgetLoader.start()
		self.communicator.FillBoard.emit()

	def initializeLayout(self):
		self.setLayout(self._layoutClass())

		self.layout().setContentsMargins(13, 13, 13, 13)
		self.layout().setSpacing(14)

	def showEvent(self, event):
		super(WidgetBoard, self).showEvent(event)
		self.communicator.FillBoard.emit()
		self.setFocus()

	def loadWidgetsUntilScreenIsExceeded(self):
		if not self._shouldLoadMoreWidgets():
			return

		self._loadWidgetBatchEvent.set()

	def _shouldLoadMoreWidgets(self):
		scrollArea = self.parent().parent()
		scrollBar = scrollArea.verticalScrollBar()

		return not self.noMoreItemsToDisplay and (
		scrollBar.value() >= (scrollBar.maximum() - scrollArea.viewport().height())
		or scrollBar.maximum() <= scrollArea.viewport().height())

	def addWidgetsFor(self, items):
		if self.isAddingWidgets:
			return

		self.isAddingWidgets = True

		for item in items:
			widget = self.getWidgetFor(item)

			QApplication.instance().processEvents()

			if not widget:
				continue

			if not shiboken.isValid(self):
				return

			self.layout().addWidget(widget)
			self.itemCount += 1

			QApplication.instance().processEvents()

			if not shiboken.isValid(self):
				return

		if self.itemCount <= self.WIDGETS_PER_BATCH:
			self.subject.notify(LoadableWidget.ROWCOUNT_CHANGED, self.itemCount)
			self.subject.notify(LoadableWidget.EVENT_DONE_LOADING, [])

		self.isAddingWidgets = False
		self.loadWidgetsUntilScreenIsExceeded()

	def _widgetLoaderRoutine(self):
		while True:
			itemsToAdd = []

			for _ in range(self.WIDGETS_PER_BATCH):
				currentItem = self.nextItem()
				if not currentItem:
					self.noMoreItemsToDisplay = True
					break

				itemsToAdd.append(currentItem)

			self._loadWidgetBatchEvent.wait()
			self._loadWidgetBatchEvent.clear()

			self.communicator.AddWidgetsFor.emit(itemsToAdd)

	def close(self):
		self.subject.clearObservers()
		self.layout().subject.clearObservers()
		self.layout().clear()
		return super(WidgetBoard, self).close()

	@abc.abstractmethod
	def nextItem(self):
		raise Exception("Subclass responsibility")

	@abc.abstractmethod
	def getWidgetFor(self, item):
		raise Exception("Subclass responsibility")
