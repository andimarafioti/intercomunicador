# -*- coding: utf-8 -*-
from PySide.QtCore import Signal, Qt
from PySide.QtGui import QLabel, QFontMetrics

from helpers.emit_sentinel import pyside_none_wrap


class ElidedHoverLabel(QLabel):

	enterEventSignal = Signal(object)
	leaveEventSignal = Signal(object)

	def __init__(self, parent):
		super(ElidedHoverLabel, self).__init__(parent)

	def enterEvent(self, event):
		self.enterEventSignal.emit(*pyside_none_wrap(event))

	def leaveEvent(self, event):
		self.leaveEventSignal.emit(*pyside_none_wrap(event))

	def setText(self, text):
		metrics = QFontMetrics(self.font())
		elided  = metrics.elidedText(text, Qt.ElideRight, self.maximumWidth() - 1)
		if elided != text:
			elided = elided[:-3] + "(...)"
		super(ElidedHoverLabel,self).setText(elided)