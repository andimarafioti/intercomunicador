# -*- coding: utf-8 -*-
class ServiceLocator(object):
	def provide(self, feature, provider):
		setattr(self, feature, provider)


Locator = ServiceLocator()