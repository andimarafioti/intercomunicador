import unittest
import mock

from helpers.observer import Subject

class TestSubject():

	def __init__(self):
		self.subject = Subject(self)

	def sendEvent(self, event):
		self.subject.notify(event)

class TestObserver():

	def __init__(self, other):
		other.subject.addObserver(self)

	def onNotify(self, emmiter, event, args):
		pass

class TestSubjectComponent(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		pass

	@classmethod
	def tearDownClass(cls):
		pass

	def test_observe(self):
		the_subject = TestSubject()
		the_observer = TestObserver(the_subject)
		the_observer.onNotify = mock.MagicMock()

		the_subject.sendEvent(2)
		the_observer.onNotify.assert_called_with(the_subject, 2, ())

if __name__ == '__main__':
	unittest.main()
