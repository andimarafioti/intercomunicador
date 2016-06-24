# -*- coding: utf-8 -*-
import StringIO

import Image
from PySide.QtCore import QSize, Qt, QPointF
from PySide.QtGui import QPainter, QColor, QPixmap, QImage, QPainterPath


class ImagesMaskarator:

	def __init__(self):
		pass

	@classmethod
	def circularMask(self, pixmap, diametro=None):
		if diametro is not None:
			size = QSize(diametro, diametro)
			pixmap = pixmap.scaled(size, mode=Qt.SmoothTransformation)

		size = pixmap.size()
		img = pixmap.toImage()
		img = img.convertToFormat(QImage.Format_ARGB32)
		imageOut = QImage(img.size(),QImage.Format_ARGB32)
		painter = QPainter()
		painter.begin(imageOut)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setRenderHint(QPainter.SmoothPixmapTransform)
		painter.setCompositionMode(QPainter.CompositionMode_Source)
		painter.setOpacity(0.0)
		painter.setBrush(Qt.white)
		painter.setPen(Qt.NoPen)
		painter.drawRect(0, 0, size.width(), size.height())
		painter.setOpacity(1)
		path = QPainterPath(QPointF(0,0))
		path.addRoundedRect(0, 0, size.width(), size.height(), size.width() / 2, size.height() / 2)
		painter.setClipPath(path)
		painter.drawImage(0,0,img)
		painter.end()

		pixmap_res = QPixmap.fromImage(imageOut)
		return pixmap_res

	@classmethod
	def changeOpacity(self, pixmap, opacity):
		image = pixmap.toImage()
		p = QPainter()
		p.begin(image)
		p.setCompositionMode(QPainter.CompositionMode_DestinationIn)
		p.fillRect(image.rect(), QColor(0, 0, 0, opacity))
		p.end()
		pixmap = pixmap.fromImage(image)
		return pixmap

	@classmethod
	def procesarImagenArtwork(self, imagen):
		size = (120, 120)
		file_imagen = StringIO.StringIO(imagen)
		im = Image.open(file_imagen)
		a = im.resize(size, Image.ANTIALIAS)
		output = StringIO.StringIO()
		a.save(output, format = "JPEG")
		res = output.getvalue()
		file_imagen.close()
		output.close()
		return res