# coding: utf-8
from time import sleep
# from Intercomunicador import dspRecord, dspPlay
from display.lcddriver import lcd
from gui.menus.Initial.initialMenu import InitialMenu
from gui.menus.configuration.configurationMenu import ConfigurationMenu

__author__ = 'andres'


class MainView:
	POSITIVO = "Iniciando..."

	TITLE = "Intercomunicador Tactico"

	LINE_SPAN = 2  # screen line height

	def __init__(self):
		self.display = lcd()
		self.display.lcd_display_string(self.POSITIVO, 1)
		self.screen_line = 0
		self._menu = None
		self._options_count = 0
		self.text = []
		sleep(1)
		self.display.lcd_display_string(self.TITLE, 1)

		self.initial_menu = InitialMenu(self)
		self.configuration_menu = ConfigurationMenu(self)

		sleep(2)
		self.setMenu(self.initial_menu)

	def setMenu(self, menu):
		self._menu = menu
		self._options_count = len(self._menu.getOptions())
		self.screen_line = 0
		self._setScreenText()

	def resetTextMenu(self):
		self.text = []
		for option in self._menu.getOptions():
			self.text.append(option.text)

	def _setScreenText(self):
		self.resetTextMenu()
		self.display.lcd_clear()
		for line_number, index in enumerate(range(self.screen_line, self.screen_line + self.LINE_SPAN)):
			self.display.lcd_display_string(self.text[index], line_number + 1)

	def downClicked(self):
		self._menu.nextOption()
		current_menu_line = self._menu.current_line
		if current_menu_line is 0:
			self.screen_line = 0
		elif current_menu_line not in range(self.screen_line, self.screen_line + self.LINE_SPAN):
			self.screen_line += 1
		self._setScreenText()

	def upClicked(self):
		self._menu.previousOption()
		current_menu_line = self._menu.current_line
		if current_menu_line is self._options_count - 1:
			self.screen_line = self._options_count - 2
		elif current_menu_line not in range(self.screen_line, self.screen_line + self.LINE_SPAN):
			self.screen_line -= 1
		self._setScreenText()

	def acceptClicked(self):
		self._menu.acceptOption()

	def backClicked(self):
		self.setMenu(self.initial_menu)

	def recordClicked(self):
		dspRecord.start()

	def playClicked(self):
		dspPlay.start()

	def stopClicked(self):
		dspRecord.recording_flag = False
