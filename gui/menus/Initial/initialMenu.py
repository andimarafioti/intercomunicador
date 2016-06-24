# coding: utf-8
from gui.menus.abstractMenu import AbstractMenu
from gui.options.configurationOption import ConfigurationOption
from gui.options.playOption import PlayOption
from gui.options.recordOption import RecordOption

__author__ = 'Andres'


class InitialMenu(AbstractMenu):
	MAIN_1 = "Grabar"
	MAIN_2 = "Reproducir"
	MAIN_3 = "Configurar"

	def _setOptions(self):
		return [RecordOption(self.MAIN_1), PlayOption(self.MAIN_2), ConfigurationOption(self.MAIN_3, self.options_menu)]
