# coding: utf-8
from PySide.QtCore import Qt
from PySide.QtGui import QPixmap, QPainter

__author__ = 'Andres'


def opaquePixmap(path, scalex, scaley, opacity):

	original_image = QPixmap()
	original_image.load(path)
	original_image = original_image.scaled(scalex,scaley, mode=Qt.SmoothTransformation)

	new_image = QPixmap(original_image.size())
	new_image.fill(Qt.transparent)

	painter = QPainter()
	painter.begin(new_image)
	painter.setOpacity(opacity)
	painter.drawPixmap(0,0,original_image)
	painter.end()

	return new_image
