#coding: utf-8
import math

from PySide.QtCore import Qt
from PySide.QtGui import QLabel, QFontMetrics

from gui.utils.elidedText import strip_tags

__author__ = 'Dev5'

class DoubleElidedText(QLabel):
	def __init__(self, *args):
		super(DoubleElidedText, self).__init__(*args)

	def setText(self, text):
		self.setToolTip(text)
		self.update()
		plainText = strip_tags(text)

		metrics = QFontMetrics(self.font())
		elide = metrics.elidedText(plainText, Qt.ElideRight, self.width()*2 - self.width()/5)

		texto = u"{}".format(elide)
		super(DoubleElidedText, self).setText(texto)

	def _setQLabelHeight(self, plainText, withMargins = False):
		plainText = strip_tags(plainText)
		metrics = QFontMetrics(self.font())

		marginWidth = 0
		if withMargins:
			margins = self.getContentsMargins()
			marginWidth = margins[0] + margins[2]

		heightCorrection = math.ceil(float(metrics.width(plainText) + marginWidth) / self.width())
		self.setMinimumHeight(metrics.height() * heightCorrection)