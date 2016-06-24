import threading
from helpers.worker.worker import Worker

__author__ = 'Dev6'


class DeferredWorker(Worker):
	def __init__(self):
		super(DeferredWorker, self).__init__()
		self._waitTime = 0

	@staticmethod
	def fromWorker(worker):
		deferredWorker = DeferredWorker()

		deferredWorker._thread = worker._thread
		deferredWorker._isDaemon = worker._isDaemon
		deferredWorker._function = worker._function
		deferredWorker._arguments = worker._arguments

		return deferredWorker

	def after(self, seconds):
		self._waitTime = seconds
		return self

	def start(self):
		if self._thread and not self._thread.isAlive():
			self._thread.cancel()

		self._thread = threading.Timer(self._waitTime, function=self._function, args=self._arguments)
		self._thread.daemon = self._isDaemon
		self._thread.start()

		return self

	def stop(self):
		if self._thread:
			self._thread.cancel()
		return self