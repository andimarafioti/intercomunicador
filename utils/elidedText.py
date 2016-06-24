# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser

from PySide.QtCore import Qt
from PySide.QtGui import QPainter, QLabel, QFontMetrics


class ElidedText(QLabel):

	def __init__(self, *args):
		super(ElidedText, self).__init__(*args)

	def setText(self, text):
		self.texto = text
		self.setToolTip(text)
		self.update()

	def paintEvent(self, event):
		self.pintar()

	def pintar(self):
		if hasattr(self,'texto'):
			painter = QPainter(self)
			metrics = QFontMetrics(self.font())
			elide = metrics.elidedText(strip_tags(self.texto), Qt.ElideRight, self.width())

			painter.drawText(self.rect(), self.alignment(), elide)

	def text(self):
		return self.texto


class MLStripper(HTMLParser):
    def __init__(self):
	    HTMLParser.__init__(self)
	    self.reset()
	    self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()