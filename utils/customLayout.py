"""PyQt4 port of the layouts/flowlayout example from Qt v4.x"""
import abc

from PySide import QtCore, QtGui

from helpers.observer import Subject


class CustomLayout(QtGui.QLayout):
	SET_GEOMETRY_COMPLETE = 0

	def __init__(self, parent=None, margin=0, spacing=-1):
		super(CustomLayout, self).__init__(parent)

		if parent is not None:
			self.setMargin(margin)

		self.setSpacing(spacing)
		self._centered = False

		self.itemList = []

		self.subject = Subject(self)

	def __del__(self):
		item = self.takeAt(0)
		while item:
			item = self.takeAt(0)

	@property
	def centerContents(self):
		return self._centered

	@centerContents.setter
	def centerContents(self, bool):
		self._centered = bool

	def addItem(self, item):
		self.itemList.append(item)

	def count(self):
		return len(self.itemList)

	def itemAt(self, index):
		if index >= 0 and index < len(self.itemList):
			return self.itemList[index]

		return None

	def takeAt(self, index):
		if index >= 0 and index < len(self.itemList):
			return self.itemList.pop(index)

		return None

	def expandingDirections(self):
		return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

	@abc.abstractmethod
	def hasHeightForWidth(self):
		raise Exception("Subclass responsibility")

	def setGeometry(self, rect):
		super(CustomLayout, self).setGeometry(rect)
		self.doLayout(rect, False)

	def sizeHint(self):
		return self.minimumSize()

	def minimumSize(self):
		size = QtCore.QSize()

		for item in self.itemList:
			size = size.expandedTo(item.minimumSize())

		size += QtCore.QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
		return size

	def doLayout(self, rect, testOnly):
		x = rect.x()
		y = rect.y()
		lineHeight = 0

		for item in self.itemList:
			wid = item.widget()
			spaceX = self.spacing() + wid.style().layoutSpacing(QtGui.QSizePolicy.PushButton, QtGui.QSizePolicy.PushButton, QtCore.Qt.Horizontal)
			spaceY = self.spacing() + wid.style().layoutSpacing(QtGui.QSizePolicy.PushButton, QtGui.QSizePolicy.PushButton, QtCore.Qt.Vertical)
			nextX = x + item.sizeHint().width() + spaceX
			if nextX - spaceX > rect.right() and lineHeight > 0:
				x = rect.x()
				y = y + lineHeight + spaceY
				nextX = x + item.sizeHint().width() + spaceX
				lineHeight = 0

			if not testOnly:
				item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

			x = nextX
			lineHeight = max(lineHeight, item.sizeHint().height())

		return y + lineHeight - rect.y()

	def clear(self):
		for i in reversed(xrange(self.count())):
			item = self.takeAt(i)
			item.widget().close()
			item.widget().deleteLater()