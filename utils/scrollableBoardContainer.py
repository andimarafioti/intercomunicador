from PySide.QtCore import Qt
from PySide.QtGui import QBoxLayout, QScrollArea

from gui.centrals.loadingWidget.loadableWidget import LoadableWidget
from helpers.worker.worker import Worker

__author__ = 'Dev6'


class ScrollableBoardContainer(LoadableWidget):
	def __init__(self, parent=None, amigo=None, boardClass=None):
		super(ScrollableBoardContainer, self).__init__(parent)

		self.setAttribute(Qt.WA_DeleteOnClose)

		self._amigo = amigo

		self.board = None

		self.setLayout(QBoxLayout(QBoxLayout.LeftToRight))
		self.scrollArea = QScrollArea(self)
		self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scrollArea.setFocusPolicy(Qt.StrongFocus)
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.verticalScrollBar().valueChanged.connect(self.onScrolled, Qt.QueuedConnection)

		self.layout().setContentsMargins(0, 0, 0, 0)
		self.layout().addWidget(self.scrollArea)

		self.setBoard(boardClass(self.scrollArea, self._amigo))

	def setBoard(self, board):
		self.board = board
		self.scrollArea.setWidget(self.board)
		self.board.subject.addObserver(self)
		self.board.layout().subject.addObserver(self)

		self.board.initialize()

	def onScrolled(self, value):
		self.board.loadWidgetsUntilScreenIsExceeded()

	def close(self):
		self.board.close()
		self.scrollArea.widget().subject.clearObservers()
		self.scrollArea.close()
		self.scrollArea.deleteLater()
		super(ScrollableBoardContainer, self).close()

	def onNotify(self, emitter, event, args):
		if emitter is self.scrollArea.widget():
			if event == self.EVENT_LOADING:
				self.subject.notify(self.EVENT_LOADING)
				return True
			elif event == self.EVENT_DONE_LOADING:
				self.subject.notify(self.EVENT_DONE_LOADING)
				return True
			elif event == self.ROWCOUNT_CHANGED:
				self.subject.notify(self.ROWCOUNT_CHANGED, args[0])
				return True

		return False
