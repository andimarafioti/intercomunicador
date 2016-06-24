import threading
from helpers.worker.worker import Worker

__author__ = 'Dev6'


class CronicWorker(Worker):
	def __init__(self):
		super(CronicWorker, self).__init__()
		self._repeatInterval = 0

	@staticmethod
	def fromWorker(worker):
		cronicWorker = CronicWorker()

		cronicWorker._thread = worker._thread
		cronicWorker._isDaemon = worker._isDaemon
		cronicWorker._function = worker._function
		cronicWorker._arguments = worker._arguments

		return cronicWorker

	def every(self, seconds):
		self._repeatInterval = seconds
		return self

	def start(self):
		self._thread = threading.Timer(self._repeatInterval, function=self._loop)
		self._thread.daemon = self._isDaemon
		self._thread.start()

		firstLoopWorker = Worker.call(self._function).withArgs(*self._arguments)
		firstLoopWorker._isDaemon = self._isDaemon
		firstLoopWorker.start()

		return self

	def stop(self):
		if self._thread:
			self._thread.cancel()
		return self

	def _loop(self):
		self._thread = threading.Timer(self._repeatInterval, function=self._loop)
		self._thread.daemon = self._isDaemon
		self._thread.start()
		self._function(*self._arguments)