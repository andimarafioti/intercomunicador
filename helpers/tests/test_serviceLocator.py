import unittest
from mock import MagicMock

from helpers.serviceLocator import Locator


class TestServiceLocator(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		pass

	@classmethod
	def tearDownClass(cls):
		pass

	def test_provide(self):
		Mock = MagicMock()
		Mock.my_id = "my_id"
		self.assertFalse(hasattr(Locator, 'Mock'))

		Locator.provide('Mock', Mock)
		self.assertTrue(hasattr(Locator, 'Mock'))

		self.assertEqual(Locator.Mock.my_id, "my_id")

if __name__ == '__main__':
	unittest.main()
