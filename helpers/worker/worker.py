import threading

__author__ = 'Dev6'

'''

This class simplifies thread usage. Examples:

1 -	Worker.call(aFunction).withArgs(arg1, arg2..argN).start() / Runs a normal thread starting at aFunction

2 -	Worker.call(aFunction).withArgs(arg1, arg2..argN).asDaemon.start() / Same as before, but uses a daemon thread

3 - Worker.call(aFunction).withArgs(arg1, arg2..argN).every(T).asDaemon.start() / Runs a thread every T seconds

4 - Worker.call(aFunction).withArgs(arg1, arg2..argN).after(T).asDaemon.start() / Runs a thread after T seconds

NOTE: The 'call' method should be called first ALWAYS!!

CronicWorker - Calling the 'every(seconds)' function returns a CronicWorker with the original Worker attributes.
DeferredWorker - Calling the 'after(seconds)'  function returns a DeferredWorker with the original Worker attributes.

NOTE: Calling 'start()' more than once on a DeferredWorker will try to 'cancel()' the first thread before launching
a new one

'''


class Worker(object):
	def __init__(self):
		self._thread = None
		self._isDaemon = False
		self._function = None
		self._callback = lambda: None
		self._arguments = ()

	@staticmethod
	def call(function):
		worker = Worker()
		worker._function = function
		return worker

	def withArgs(self, *args):
		self._arguments = args
		return self

	def withCallback(self, callback):
		self._callback = callback

		return self

	@property
	def asDaemon(self):
		self._isDaemon = True
		return self

	def start(self):
		this = self
		callback = self._callback

		def callFunctionAndThenCallback(*args):
			this._function(*args)
			callback()

		self._thread = threading.Thread(target=callFunctionAndThenCallback, args=self._arguments)
		self._thread.daemon = self._isDaemon
		self._thread.start()

		return self

	def isWorking(self):
		return self._thread.isAlive() if self._thread else False

	def join(self):
		if self.isWorking():
			self._thread.join()

	def every(self, seconds):
		from helpers.worker.cronicWorker import CronicWorker
		cronicWorker = CronicWorker.fromWorker(self)
		cronicWorker._repeatInterval = seconds
		return cronicWorker

	def after(self, seconds):
		from helpers.worker.deferredWorker import DeferredWorker
		deferredWorker = DeferredWorker.fromWorker(self)
		deferredWorker._waitTime = seconds
		return deferredWorker

	def _reset(self):
		self._thread = None
		self._isDaemon = False
		self._function = None
		self._callback = lambda: None
		self._arguments = ()
