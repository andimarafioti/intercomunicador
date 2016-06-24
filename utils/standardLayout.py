from PySide.QtCore import QPoint, QRect

from gui.utils.customLayout import CustomLayout

__author__ = 'Dev6'


class StandardLayout(CustomLayout):
	def __init__(self, parent=None, margin=0, spacing=-1):
		super(StandardLayout, self).__init__(parent, margin, spacing)

		self.heightForWidthValue = 0

	def hasHeightForWidth(self):
		return True

	def heightForWidth(self, width):
		return self.heightForWidthValue

	def setGeometry(self, rect):
		super(StandardLayout, self).setGeometry(rect)

		self.heightForWidthValue = rect.height()

		if not any(self.itemList):
			return

		# save some data to avoid recalculation
		firstItem = self.itemList[0]

		margin = self.contentsMargins()

		x = rect.x()
		y = rect.y()

		spaceX = spaceY = self.spacing()

		itemSize = firstItem.sizeHint()
		itemWidth = itemSize.width()
		itemHeight = itemSize.height()

		effectiveWidth = rect.width() - margin.left() - margin.right()

		# calculate column count
		columnCount = (effectiveWidth + spaceX) / (itemWidth + spaceX)

		# add left spacing
		x += margin.left()

		if self.centerContents:
			x += ((effectiveWidth - ((columnCount * (itemWidth + spaceX)) - spaceX)) / 2)

		# add top spacing
		y += margin.top()

		# calculate item positions
		currentColumn = 0
		currentRow = 0

		# place the items one by one
		for item in self.itemList:
			if currentColumn not in range(columnCount):
				currentColumn = 0
				currentRow += 1

			currentPosition = QPoint(x + currentColumn * (itemWidth + spaceX), y + currentRow * (itemHeight + spaceY))

			currentColumn += 1

			item.setGeometry(QRect(currentPosition, itemSize))

		self.heightForWidthValue = (currentRow + 1) * (itemHeight + spaceY) + margin.bottom()

		self.subject.notify(self.SET_GEOMETRY_COMPLETE)
