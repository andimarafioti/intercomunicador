import unittest

from helpers.decorators import paramsToLists

class testConexion(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def test_paramsToLists(self):
		a,b,c,d,e = self.func(a="hola", d=["que tal"])
		self.assertEqual((a,b,c,d,e), (["hola"], None, None, ["que tal"], None))

		a,b,c,d,e = self.func(a = "hola", b=["abc", "def"], c="asd", d=["fgh"])
		self.assertEqual((a,b,c,d,e), (["hola"], ["abc", "def"], ["asd"], ["fgh"], None))

		a,b,c,d,e = self.func("hola", ["abc", "def"], d="asd", e=["fgh"])
		self.assertEqual((a,b,c,d,e), (["hola"], ["abc", "def"], None, ["asd"], ["fgh"]))

	@paramsToLists
	def func(self, a=None,b=None,c=None,d=None,e=None):
		return a, b, c, d, e

if __name__ == '__main__':
	unittest.main()