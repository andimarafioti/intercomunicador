# coding: utf-8
from operator import attrgetter
from PySide import QtCore
from PySide.QtCore import QRect, QObject, Signal, Qt
from PySide.QtGui import QPixmap, QApplication
import sys
from gui.utils.clickableLabel import ClickableLabel
from gui.utils.opaquePixmap import opaquePixmap
from helpers.observer import Subject
from helpers.serviceLocator import Locator
from media.contenido.musicAsset import MusicAsset

__author__ = 'Andres'

class PlayableLabel(ClickableLabel):
	"""
	PlayableLabel es un label preparado para mostrar las opciones de reproducción cuando se le hace hover.
	Su tamaño se debe setear con setGeometry(QRect()).
	Si quiere usarse la funcionalidad de cambio de estado según disponibilidad, se debe setear el asset.
	Tiene un Subject que avisa dos eventos PLAY_CLICKED y OPCIONES_CLICKED.
	"""

	LABEL_PLAY_PIXMAP = None
	OPCIONES_REPRODUCCION_PIXMAP = None
	PLAY_CLICKED = 0
	OPCIONES_CLICKED = 1

	def __init__(self, parent = None):
		super(PlayableLabel, self).__init__(parent)

		if PlayableLabel.LABEL_PLAY_PIXMAP is None:
			PlayableLabel.LABEL_PLAY_PIXMAP = QPixmap('icons/52_playlist_play.png')
			PlayableLabel.OPCIONES_REPRODUCCION_PIXMAP = QPixmap('icons/38_opciones_reproduccion.png')

		self.isAvailable = True
		self._asset = None
		self.subject = Subject(self)

		self.label_image = ClickableLabel(self)
		self.label_image.setIndent(-1)
		self.label_unavailable = ClickableLabel(self)
		self.label_unavailable.setStyleSheet("background-color: rgba(242, 242, 242, 178);\n")
		self.label_unavailable.setAlignment(QtCore.Qt.AlignCenter)
		self.label_play = ClickableLabel(self)
		self.label_play.setStyleSheet("background-color: rgba(0, 0, 0, 90);")
		self.label_play.setAlignment(QtCore.Qt.AlignCenter)
		self.label_acciones_reproduccion = ClickableLabel(self)
		self.label_acciones_reproduccion.setStyleSheet("QLabel{background-color: rgba(0, 0, 0, 0);}")
		self.label_acciones_reproduccion.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)

		self.label_play.labelClicked.connect(self.label_play_clicked)
		self.label_image.labelClicked.connect(self.label_acciones_clicked)
		self.label_unavailable.labelClicked.connect(self.label_acciones_clicked)
		self.label_acciones_reproduccion.labelClicked.connect(self.label_acciones_clicked)

		self.setPixmaps()
		self.label_play.hide()
		self.label_acciones_reproduccion.hide()
		self.paintAvailability()

	def setAsset(self, asset):
		self._asset = asset
		self._asset.subject.addObserver(self)
		self.updateAvailability()

	def label_acciones_clicked(self):
		self.subject.notify(self.OPCIONES_CLICKED, self)

	def label_play_clicked(self):
		self.subject.notify(self.PLAY_CLICKED, self)

	def updateAvailability(self):
		Locator.LazyLoader.set(self.setAvailability, attrgetter('isAvailable'), [self._asset], defaultVal=False)

	def setAvailability(self, availability):
		self.isAvailable = availability
		self.paintAvailability()

	def paintAvailability(self):
		if self.isAvailable:
			self.label_unavailable.hide()
		else:
			self.setLabelUnavailablePixmap()
			self.label_unavailable.show()

	def setPixmap(self, *args, **kwargs):
		self.label_image.setPixmap(*args, **kwargs)

	def setPixmaps(self):
		geometry = self.geometry()
		if geometry.height() < 90:
			pixmap_foto = PlayableLabel.LABEL_PLAY_PIXMAP.scaled(geometry.width()*0.5, geometry.height()*0.5, mode=Qt.SmoothTransformation)
			self.label_play.setPixmap(pixmap_foto)
		else:
			self.label_play.setPixmap(PlayableLabel.LABEL_PLAY_PIXMAP)
		self.label_acciones_reproduccion.setPixmap(PlayableLabel.OPCIONES_REPRODUCCION_PIXMAP)

	def setGeometry(self, QRect):
		super(PlayableLabel, self).setGeometry(QRect)
		self.label_image.setGeometry(QRect)
		self.label_unavailable.setGeometry(QRect)
		self.label_play.setGeometry(QRect)
		self.label_acciones_reproduccion.setGeometry(QRect.x(), QRect.height()-18 , 38, 22)
		self.setPixmaps()

	def setLabelUnavailablePixmap(self):
		pixmap = opaquePixmap("icons/30_notificacion_unavailable.png", 30, 30, 0.7)
		self.label_unavailable.setPixmap(pixmap)

	def enterEvent(self, event):
		if self.isAvailable:
			self.label_play.show()
		self.label_acciones_reproduccion.show()

	def leaveEvent(self, event):
		self.label_play.hide()
		self.label_acciones_reproduccion.hide()

	def onNotify(self, emitter, event, args):
		if emitter is self._asset:
			if event is MusicAsset.AVAILABILITY_CHANGED:
				self.updateAvailability()


if __name__ == '__main__':
	app = QApplication( sys.argv )
	app.setApplicationName( 'PlayableLabel' )

	interface = PlayableLabel()
	interface.setGeometry(QRect(0, 0, 60, 60))
	interface.setPixmap(QPixmap('../../icons/128_album_desconocido.png'))

	# tr = Tooltip(parent=interface, position=QPoint(400, 100), arrow=Tooltip.RIGHT, arrow_alignment=Tooltip.ALIGN_TOP)
	# tu = Tooltip(parent=interface, position=QPoint(400, 400), arrow=Tooltip.UP, arrow_alignment=Tooltip.ALIGN_RIGHT)
	# td = Tooltip(parent=interface, position=QPoint(100, 100), arrow=Tooltip.LEFT, arrow_alignment=Tooltip.ALIGN_BOTTOM)

	interface.show()

	sys.exit( app.exec_() )