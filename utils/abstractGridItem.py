# coding: utf-8

from PySide.QtCore import Qt, QEvent, QSize, QObject, Signal
from PySide.QtGui import QPixmap, QCursor
from lazy import lazy

from gui.utils.ActionsMenu import ActionsMenu
from gui.utils.opaquePixmap import opaquePixmap
from helpers.observer import Subject
from helpers.serviceLocator import Locator
from media.contenido.musicAsset import MusicAsset
from ui.ui_playlist_item import Ui_playlist_item

__author__ = 'Andres'


class AbstractGridItemCommunicator(QObject):
	PaintAvailable = Signal()
	PaintNotAvailable = Signal()


class AbstractGridItem(Ui_playlist_item):
	TITLE_CLICKED = 0
	IMAGE_CLICKED = 1

	LABEL_PLAY_PIXMAP = None
	OPCIONES_REPRODUCCION_PIXMAP = None

	def __init__(self, parent, asset, amigo):
		super(AbstractGridItem, self).__init__(parent)

		self.setupUi(self)

		if AbstractGridItem.LABEL_PLAY_PIXMAP is None:
			AbstractGridItem.LABEL_PLAY_PIXMAP = QPixmap('icons/52_playlist_play.png')
			AbstractGridItem.OPCIONES_REPRODUCCION_PIXMAP = QPixmap('icons/38_opciones_reproduccion.png')

		self.subject = Subject(self)

		self._asset = asset
		self._amigo = amigo

		self.painted_not_available = None

		self.setAttribute(Qt.WA_StyledBackground)
		self.widget_transparencia = None
		self.available_title_stylesheet = self.label_title.styleSheet()
		self.available_subtitle_stylesheet = self.label_subtitle.styleSheet()

		self.label_play.setPixmap(AbstractGridItem.LABEL_PLAY_PIXMAP)
		self.label_play.raise_()
		self.label_acciones_reproduccion.raise_()
		self.label_play.hide()
		self.label_unavailable.hide()

		self.label_title.labelClicked.connect(self.titleClicked)
		self.label_subtitle.labelClicked.connect(self.titleClicked)
		self.label_play.labelClicked.connect(self.imageClicked)
		self.label_acciones_reproduccion.labelClicked.connect(self.acciones_reproduccion)
		self.label_unavailable.labelClicked.connect(self.acciones_reproduccion)

		self.label_image.installEventFilter(self)
		self.label_unavailable.installEventFilter(self)
		self.label_play.installEventFilter(self)
		self.label_acciones_reproduccion.installEventFilter(self)

		self._asset.subject.addObserver(self)

		self.communicator = AbstractGridItemCommunicator()
		self.communicator.PaintAvailable.connect(self.paint_available, Qt.QueuedConnection)
		self.communicator.PaintNotAvailable.connect(self.paint_not_available, Qt.QueuedConnection)

		self.updateAvailability()

	def set_selected(self):
		self.setStyleSheet("background-color: rgb(26, 188, 156);")
		self.label_title.setStyleSheet(self.label_title.styleSheet() + "QLabel:hover {color:white;}")
		self.label_subtitle.setStyleSheet(self.label_subtitle.styleSheet() + "QLabel:hover {color:white;}")
		if self.painted_not_available:
			self.label_title.setStyleSheet(
				self.available_title_stylesheet + 'QLabel {background-color: rgb(26, 188, 156);} QLabel:hover {color:white;}')
			self.label_subtitle.setStyleSheet(
				self.available_subtitle_stylesheet + 'QLabel {background-color: rgb(26, 188, 156);} QLabel:hover {color:white;}')

	def unset_selected(self):
		if self.painted_not_available:
			self.set_unavailable_stylesheet()
		else:
			self.set_available_stylesheet()

	def updateAvailability(self):
		Locator.LazyLoader.set(self._setAvailability, self._asset.isAvailableFor, [self._amigo.getId()], defaultVal=False)

	def _setAvailability(self, availability):
		if availability:
			self.communicator.PaintAvailable.emit()
		else:
			self.communicator.PaintNotAvailable.emit()

	def paint_not_available(self):
		self.set_unavailable_stylesheet()
		self.set_label_unavailable_image()
		self.unavailable_stack_widgets()
		self.painted_not_available = True

	def unavailable_stack_widgets(self):
		self.label_image.lower()
		self.label_unavailable.show()
		self.label_acciones_reproduccion.raise_()

	def paint_available(self):
		self.set_available_stylesheet()
		self.available_stack_widgets()
		self.painted_not_available = False

	def available_stack_widgets(self):
		self.label_unavailable.hide()

	def set_available_stylesheet(self):
		self.setStyleSheet("background-color: rgb(46, 43, 43);")
		self.label_title.setStyleSheet(self.available_title_stylesheet)
		self.label_subtitle.setStyleSheet(self.available_subtitle_stylesheet)

	def set_unavailable_stylesheet(self):
		self.setStyleSheet('background-color: rgb(183, 182, 183);')
		self.label_title.setStyleSheet(
			self.available_title_stylesheet + 'QLabel {background-color: rgb(183, 182, 182);}')
		self.label_subtitle.setStyleSheet(
			self.available_subtitle_stylesheet + 'QLabel {background-color: rgb(183, 182, 182);}')

	def set_label_unavailable_image(self):
		pixmap = opaquePixmap("icons/30_notificacion_unavailable.png", 30, 30, 0.7)
		self.label_unavailable.setPixmap(pixmap)

	def acciones_reproduccion(self):
		self.showSongMenu(QCursor.pos())

	def titleClicked(self):
		raise NotImplementedError

	# @pyside_none_deco
	def imageClicked(self):
		self._asset.listened()

	def eventFilter(self, obj, event):
		if obj is self.label_image or \
						obj is self.label_play or \
						obj is self.label_acciones_reproduccion or \
						obj is self.label_unavailable:
			if event.type() is QEvent.Enter:
				if self._asset.isAvailable:
					self.label_play.show()
				self.label_acciones_reproduccion.setPixmap(AbstractGridItem.OPCIONES_REPRODUCCION_PIXMAP)
			if event.type() is QEvent.Leave:
				if self._asset.isAvailable:
					self.label_play.hide()
				self.label_acciones_reproduccion.setPixmap(None)
		return False

	def _setPixmap(self, image_data):
		if image_data is None:
			return

		pix = QPixmap()
		pix.loadFromData(image_data)
		pix = pix.scaled(125, 125, mode=Qt.SmoothTransformation)
		self.label_image.setPixmap(pix)

	def sizeHint(self):
		return QSize(132, 173)

	def showSongMenu(self, pos):
		song_menu = ActionsMenu(self, self._asset, self._amigo)
		song_menu.exec_(pos)

	@lazy
	def songs(self):
		return self._asset.songs(self._amigo.getId())

	def onNotify(self, emitter, event, args):
		if emitter is self._asset:
			if event is MusicAsset.AVAILABILITY_CHANGED:
				self.updateAvailability()

	def playNow(self):
		self._asset.listened()
		Locator.Cola.reproducirAhora(self.songs)

	def addNext(self):
		self._asset.listened()
		Locator.Cola.agregarSiguiente(self.songs)

	def addLast(self):
		self._asset.listened()
		Locator.Cola.agregarAlFinal(self.songs)
