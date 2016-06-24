# coding: utf-8
from gui.menus.abstractMenu import AbstractMenu
from gui.options.abstractOption import AbstractOption

__author__ = 'Andres'


class ConfigurationMenu(AbstractMenu):
	MAIN_1 = "Nombre de Archivo"
	MAIN_2 = "Fecha y hora"
	MAIN_3 = "Lugar"

	def _setOptions(self):
		return [AbstractOption(self.MAIN_1), AbstractOption(self.MAIN_2), AbstractOption(self.MAIN_3)]
