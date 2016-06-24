# from Intercomunicador import dspPlay
from gui.options.abstractOption import AbstractOption

__author__ = 'andres'


class PlayOption(AbstractOption):
	def accept(self, file_name):
		dspPlay.start()
