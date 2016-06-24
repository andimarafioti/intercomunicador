# coding: utf-8
import logging

__author__ = 'Andres'


class AbstractMenu(object):
	def __init__(self, options_menu):
		self.options_menu = options_menu
		self.options = self._setOptions()
		self._current_line = 0
		self._selectOption()

	def getOptions(self):
		return self.options

	def nextOption(self):
		self._scrollOptions(span=1)

	def previousOption(self):
		self._scrollOptions(span=-1)

	def acceptOption(self):
		self.options[self.current_line].accept()

	@property
	def current_line(self):
		return self._current_line

	@current_line.setter
	def current_line(self, value):
		self._current_line = value % len(self.options)

	def _scrollOptions(self, span):
		self._deselectOption()
		self.current_line += span
		self._selectOption()

	def _deselectOption(self):
		self.options[self._current_line].deselect()

	def _selectOption(self):
		self.options[self._current_line].select()

	def _setOptions(self):
		raise NotImplementedError("Subclass Responsibility")
