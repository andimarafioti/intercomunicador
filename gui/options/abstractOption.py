# coding: utf-8
__author__ = 'Andres'


class AbstractOption(object):
	def __init__(self, text):
		self._text = text
		self.text = text

	def select(self):
		self.text = ">> " + self._text

	def deselect(self):
		self.text = self._text

	def accept(self, *args):
		raise NotImplementedError("Subclass Responsibility")