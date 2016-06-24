# coding: utf-8
from functools import partial

from gui.esttelaMenu import EsttelaMenu
from gui.nuevaPlaylistScreen import NuevaPlaylistScreen
from gui.popup.popup import Popup
from media.contenido.cancion import Cancion
from ui.ui_playlist_songlist_header import Ui_playlist_songlist_header

__author__ = 'Andres'

from helpers.serviceLocator import Locator


class ActionsMenu(EsttelaMenu):
	def __init__(self, parent, asset, view_amigo):
		super(ActionsMenu, self).__init__(parent=parent, background_color="rgb(255, 255, 255)")

		if isinstance(asset, Cancion):
			self._songs = [asset]
		else:
			self._songs = asset.songs(view_amigo.getId())

		if self.isAvailable:
			self.addAction('Reproducir ahora', self.parent().playNow)
			self.addAction('Agregar adelante', self.parent().addNext)
			self.addAction('Agregar al final', self.parent().addLast)
			self.addSeparator()

		self.pls_menu = self.addMenu('Agregar a playlist')
		for playlist in Locator.DataAccess.playlists.search(Locator.Amigos.yo.getId()):
			action = partial(self.addToPlaylist, playlist)
			self.pls_menu.addAction(playlist.name , action)
		self.pls_menu.addSeparator()
		self.pls_menu.addAction("Crear nueva...", self.addToNewPlaylist)

	@property
	def isAvailable(self):
		for song in self._songs:
			if song.isAvailable:
				return True
		return False

	def addToPlaylist(self, playlist):
		playlist.addSongs(self._songs)

	def addToNewPlaylist(self):
		popup = Popup("Crear nueva playlist")
		new_playlist_screen = NuevaPlaylistScreen(self, self._songs)
		popup.setContenido(new_playlist_screen)
		new_playlist_screen.but_cancelar.clicked.connect(popup.ocultar)
		new_playlist_screen.but_aceptar.clicked.connect(popup.ocultar)
		popup.show()
