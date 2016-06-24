from gui.options.abstractOption import AbstractOption

__author__ = 'andres'


class ConfigurationOption(AbstractOption):
	def __init__(self, text, options_menu):
		super(ConfigurationOption, self).__init__(text)
		self.options_menu = options_menu

	def accept(self, *args):
		self.options_menu.setMenu(self.options_menu.configuration_menu)
