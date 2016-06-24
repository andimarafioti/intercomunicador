# from Intercomunicador import dspRecord
from gui.options.abstractOption import AbstractOption

__author__ = 'andres'


class RecordOption(AbstractOption):
	def accept(self, *args):
		dspRecord.start()
