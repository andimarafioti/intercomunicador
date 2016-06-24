from PySide.QtCore import QPoint, QRect
from PySide.QtGui import QPixmap, QLabel

from gui.centrals.loadingWidget.artistWidget.artistItem import ArtistItem
from gui.utils.customLayout import CustomLayout

__author__ = 'Dev6'


class ArtistsBoardLayout(CustomLayout):
	def __init__(self, parent=None, margin=0, spacing=-1):
		super(ArtistsBoardLayout, self).__init__(parent, margin, spacing)

		self.heightForWidthValue = 0

		self.expandedArtist = None

		self.indexByItem = {}

		self.columnCount = 0
		self.rowCount = 0

		self.submenuTargetIndex = -1

		self.triangle = QLabel(self.parent())
		self.triangle.setPixmap(QPixmap('icons/22_seleccionado.png'))
		self.addWidget(self.triangle)

	def hasHeightForWidth(self):
		return True

	def heightForWidth(self, width):
		return self.heightForWidthValue

	def setGeometry(self, rect):
		super(ArtistsBoardLayout, self).setGeometry(rect)

		self.heightForWidthValue = rect.height()

		self.triangle.setHidden(not self.parent().selectedArtistItem)

		itemsToArrange = filter(lambda i: isinstance(i.widget(), ArtistItem), self.itemList)

		if not any(itemsToArrange):
			return

		# save some data to avoid recalculation
		firstItem = itemsToArrange[0]

		margin = self.contentsMargins()

		x = rect.x()
		y = rect.y()

		spaceX = spaceY = self.spacing()

		itemSize = firstItem.sizeHint()

		itemWidth = itemSize.width()
		itemHeight = itemSize.height()

		effectiveWidth = rect.width() - margin.left() - margin.right()

		# calculate column count
		self.columnCount = (effectiveWidth + spaceX) / (itemWidth + spaceX)

		# add left spacing
		x += margin.left()

		if self.centerContents:
			x += ((effectiveWidth - ((self.columnCount * (itemWidth + spaceX)) - spaceX)) / 2)

		# add top spacing
		y += margin.top()

		# calculate item positions
		currentColumn = 0
		currentRow = 0

		putSubmenuInNextRow = False

		# place the items one by one
		for item in itemsToArrange:

			if currentColumn == self.columnCount:
				currentColumn = 0
				currentRow += 1

				if putSubmenuInNextRow:
					putSubmenuInNextRow = False

					currentPosition = QPoint(0, y + currentRow * (itemHeight + spaceY))

					self.parent().artistAlbumsView.setGeometry(currentPosition.x(),
															   currentPosition.y(),
															   rect.width(),
															   self.parent().artistAlbumsView.size().height())
					y += self.parent().artistAlbumsView.size().height() + self.spacing()

					selectedItemRect = self.parent().selectedArtistItem.geometry()
					triangleRect = QRect(selectedItemRect.x() + (itemWidth / 2) - (self.triangle.width() / 2),
										 selectedItemRect.y() + itemHeight + spaceY - self.triangle.height(),
										 self.triangle.sizeHint().width(),
										 self.triangle.sizeHint().height())
					self.triangle.setGeometry(triangleRect)

			currentPosition = QPoint(x + currentColumn * (itemWidth + spaceX), y + currentRow * (itemHeight + spaceY))

			item.setGeometry(QRect(currentPosition, itemSize))

			currentColumn += 1

			if not putSubmenuInNextRow:
				putSubmenuInNextRow = item.widget() is self.parent().selectedArtistItem

		if putSubmenuInNextRow:
			currentPosition = QPoint(0, y + (currentRow + 1) * (itemHeight + spaceY))

			self.parent().artistAlbumsView.setGeometry(currentPosition.x(),
													   currentPosition.y(),
													   rect.width(),
													   self.parent().artistAlbumsView.size().height())
			y += self.parent().artistAlbumsView.size().height() + self.spacing()

			selectedItemRect = self.parent().selectedArtistItem.geometry()
			triangleRect = QRect(selectedItemRect.x() + (itemWidth / 2) - (self.triangle.width() / 2),
										 selectedItemRect.y() + itemHeight + spaceY - self.triangle.height(),
										 self.triangle.sizeHint().width(),
										 self.triangle.sizeHint().height())
			self.triangle.setGeometry(triangleRect)

		self.rowCount = currentRow + 1

		self.heightForWidthValue = self.rowCount * (itemHeight + spaceY) + margin.bottom()

		if self.parent().selectedArtistItem:
			self.heightForWidthValue += self.parent().artistAlbumsView.size().height() + spaceY

		self.subject.notify(self.SET_GEOMETRY_COMPLETE)
