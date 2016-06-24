# -*- coding: utf-8 -*-
import logging
from threading import RLock
from PySide.QtCore import QThread
from PySide.QtGui import QApplication


class Subject:
	def __init__(self, parent):
		self.parent = parent
		self._observers_lock = RLock()
		self._observers = set()

	def addObserver(self, observer):
		with self._observers_lock:
			self._observers.add(observer)

	def removeObserver(self, observer):
		with self._observers_lock:
			self._observers.remove(observer)

	def clearObservers(self):
		with self._observers_lock:
			self._observers.clear()

	def notify(self, event, *args):
		with self._observers_lock:
			observers = list(self._observers)

		for obs in observers:
			try:
				obs.onNotify(self.parent, event, args)
			except Exception, e:
				logging.exception('- [ERROR] "EXCEPCION notificando evento [Evento: {}; Observer: {}, Args: {}]"'.format(event, obs, args))
				print e