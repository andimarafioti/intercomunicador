import unittest

from helpers.utils import transformToLists

class testConexion(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def test_transformToLists(self):
		a = "hola"
		b = None
		c = ["avion"]
		d = ["dinosaurio", "electricidad"]
		e = 157

		a,b,c,d,e = transformToLists(a,b,c,d,e)
	
		self.assertEqual((a,b,c,d,e), (["hola"], None, ["avion"], ["dinosaurio", "electricidad"], [157]))

if __name__ == '__main__':
	unittest.main()