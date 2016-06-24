from PySide import QtCore
from PySide.QtCore import QPoint

from gui.utils.customLayout import CustomLayout


class PinterestLayout(CustomLayout):
	def __init__(self, parent=None, margin=0, spacing=-1):
		super(PinterestLayout, self).__init__(parent, margin, spacing)

		self._content_left = 0
		self._content_right = 0
		self._content_top = 0
		self._content_bottom = 0

		self.heightForWidthValue = 0

		self.itemList = []

	@property
	def content_left(self):
		return self._content_left

	@content_left.setter
	def content_left(self, value):
		raise Exception("Only the layout can change content position")

	@property
	def content_right(self):
		return self._content_right

	@content_right.setter
	def content_right(self, value):
		raise Exception("Only the layout can change content position")

	@property
	def content_top(self):
		return self._content_top

	@content_top.setter
	def content_top(self, value):
		raise Exception("Only the layout can change content position")

	@property
	def content_bottom(self):
		return self._content_left

	@content_bottom.setter
	def content_bottom(self, value):
		raise Exception("Only the layout can change content position")

	def hasHeightForWidth(self):
		return True

	def heightForWidth(self, width):
		return self.heightForWidthValue

	def setGeometry(self, rect):
		super(PinterestLayout, self).setGeometry(rect)

		self.heightForWidthValue = rect.height()

		if not any(self.itemList):
			return

		# save some data to avoid recalculation
		firstItem = self.itemList[0]

		margin = self.contentsMargins()

		x = rect.x()
		y = rect.y()

		spaceX = spaceY = self.spacing()

		itemWidth = firstItem.sizeHint().width()

		effectiveWidth = rect.width() - margin.left() - margin.right()

		# calculate column count
		columnCount = (effectiveWidth + spaceX) / (itemWidth + spaceX)

		# add left spacing
		x += margin.left()

		if self.centerContents:
			x += ((effectiveWidth - ((columnCount * (itemWidth + spaceX)) - spaceX)) / 2)

		# add top spacing
		y += margin.top()

		# set initial available positions (first row)
		availablePositions = list()
		for i in range(columnCount):
			availablePositions.append(QPoint(x + i * (itemWidth + spaceX), y))

		# place the items one by one
		for item in self.itemList:

			currentPosition = availablePositions[0]
			currentPositionColumn = 0

			# get upmost (minimum y) available position and remember column number
			positionColumn = 0
			for position in availablePositions:
				if min(currentPosition.y(), position.y()) != currentPosition.y():
					currentPositionColumn = positionColumn
					currentPosition = position

				positionColumn += 1

			# update available position in current column
			itemSize = item.sizeHint()
			availablePositions[currentPositionColumn] = QPoint(currentPosition.x(),
															   currentPosition.y() + itemSize.height() + spaceY)

			# place item
			item.setGeometry(QtCore.QRect(currentPosition, itemSize))

		# remember the new widget height
		self.heightForWidthValue = max(map(lambda position: position.y(), availablePositions))

		# remember content borders
		self._content_left = x
		self._content_top = y
		self._content_right = x + (columnCount * (itemWidth + spaceX) - spaceX)
		self._content_bottom = 0

		self.subject.notify(self.SET_GEOMETRY_COMPLETE)
