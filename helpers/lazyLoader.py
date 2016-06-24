import Queue
import threading
import traceback

from PySide.QtCore import QObject, Signal, Qt, QThread
from PySide.QtGui import QApplication

from Shiboken import shiboken

from helpers.emit_sentinel import pyside_none_deco, pyside_none_wrap
from helpers.worker.worker import Worker


class LazyLoader(QObject):
	SetValue = Signal(object, object, object)  # setter, value, setter_validator

	def __init__(self):
		super(LazyLoader, self).__init__()

		self.SetValue.connect(self._setValue, Qt.QueuedConnection)

		self._tasks = Queue.Queue()

		Worker.call(self._execute).asDaemon.start()

	def set(self, valueSetter, valueGetter, valueGetterParams=None, defaultVal=None, validCheckFunction=None):
		if valueGetterParams is None:
			valueGetterParams = []

		if defaultVal is not None:
			self.SetValue.emit(*pyside_none_wrap(valueSetter, defaultVal, None))

		self._tasks.put((valueSetter, defaultVal, valueGetter, valueGetterParams, validCheckFunction))

	def _execute(self):
		while True:
			try:
				setter, default_val, data_func, data_params, validcheck_function = self._tasks.get()

				# Test that the setter is still alive, and isn't duplicate:
				if self._isSetterValid(setter, validcheck_function):
					res = data_func(*data_params)
					self.SetValue.emit(*pyside_none_wrap(setter, res, validcheck_function))

				self._tasks.task_done()
			except Exception, e:
				print "[ERROR - LAZYLOADER] Excepcion: {}".format(e)
				traceback.print_exc()


	@pyside_none_deco
	def _setValue(self, setter, value, setterValidator):
		if self._isSetterValid(setter, setterValidator):
			setter(value)

	def _isSetterValid(self, setter, validcheck_function=None):
		return not hasattr(setter, '__self__') or (shiboken.isValid(setter.__self__) \
			   and (not validcheck_function or validcheck_function()))
