from PySide.QtCore import Qt
from PySide.QtGui import QScrollArea, QWheelEvent


class HScrollArea(QScrollArea):
	def __init__(self, parent=None):
		super(HScrollArea, self).__init__(parent)
		self.installEventFilter(self)

	def eventFilter(self, obj, event):
		if isinstance(event, QWheelEvent) and event.orientation() == Qt.Vertical and self.hasFocus():
			event.accept()
			fakeEvent = QWheelEvent(event.pos(),
									event.globalPos(),
									event.delta() * -1,  # feels more natural to scroll right on wheel-down
									event.buttons(),
									event.modifiers(),
									Qt.Horizontal)  # orientation of the event is changed ;)

			self.horizontalScrollBar().wheelEvent(fakeEvent)
			return True

		event.ignore()
		return False
