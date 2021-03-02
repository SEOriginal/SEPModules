import unittest

from SEPModules.SEPIO import ConsoleArguments

#TODO: test __load_arguments__ and requires
class TestConsoleArgumentsMethods(unittest.TestCase):
	
	#Set up a console arg manager with inputs:
	#		args	: -a, -c 3, -d 				( -b   not set)
	#		kwargs: --test=ok, --one=1 	(--two not set)
	def setUp(self):
		#setup empty console arg manager
		self.CAM = ConsoleArguments([], [], noLoad=True)
		#add fake inputs to the manager
		self.CAM._argnames, self.CAM._kwargnames = "ab:c:d", ["test", "one=", "two"]
		self.CAM.requires_arg = {"a": False, "b": True, "c": True, "d": False, "test": False, "one": True, "two": False}
		self.CAM._args, self.CAM._kwargs = {"a":"", "c": "3", "d":""}, {"test": "ok", "one": "1"}
		
	def tearDown(self):
		del self.CAM
		
	#++++TEST INIT++++
	def test_cam_init_TypeError_ValueError(self):
		with self.assertRaises(TypeError):
			testCAM = ConsoleArguments(False, ["ananas", "one", "two="], noLoad=True)
		with self.assertRaises(TypeError):
			testCAM = ConsoleArguments(["a", "b", "c:"], {"ananas":"", "one":"", "two=":""}, noLoad=True)
		with self.assertRaises(ValueError):
			testCAM = ConsoleArguments(["a", "b", "c:"], ["a=", "b=", "ef"], noLoad=True)
			
	def test_cam_init_return(self):
		testCAM = ConsoleArguments(["a", "b", "c:"], ["ananas", "one", "two="], noLoad=True)
		self.assertEqual(testCAM._argnames, "abc:")
		self.assertListEqual(testCAM._kwargnames, ["ananas", "one", "two="])
		self.assertDictEqual(testCAM.requires_arg, {"a": False, "b": False, "c": True, "ananas": False, "one": False, "two": True})
		
	#++++TEST PROPERTIES++++
	def test_size_return(self):
		self.assertEqual(self.CAM.size[ConsoleArguments.__SET__],	 						5)
		self.assertEqual(self.CAM.size[ConsoleArguments.__ARGS__], 						3)
		self.assertEqual(self.CAM.size[ConsoleArguments.__KWARGS__], 					2)
		self.assertEqual(self.CAM.size[ConsoleArguments.__REQUIRED__], 				3)
		self.assertEqual(self.CAM.size[ConsoleArguments.__REQUIRED_AND_SET__],2)
		
	#++++TEST DUNDER++++
	def test_contains_TypeError(self):
		with self.assertRaises(TypeError):
			True in self.CAM
		
	def test_contains_return(self):
		with self.subTest(type='str'):
			self.assertTrue("c" in self.CAM)
			self.assertFalse("b" in self.CAM)
			self.assertTrue("one" in self.CAM)
			self.assertFalse("two" in self.CAM)
		
		with self.subTest(type='list'):
			self.assertTrue(["a", "d", "one"] in self.CAM)
			self.assertFalse(["a", "b", "one"] in self.CAM)
		
		with self.subTest(type='dict'):
			self.assertTrue({"a":"", "c": "3", "test": "ok"} in self.CAM)
			self.assertFalse({"a": "3", "c": "3", "one": "1"} in self.CAM)
		
	def test_getitem_KeyError_TypeError(self):
		with self.assertRaises(KeyError):
			self.CAM["what"]
		with self.assertRaises(TypeError):
			self.CAM[3]
			
	def test_getitem_return(self):
		self.assertTrue(self.CAM["a"])
		self.assertEqual(self.CAM["c"], "3")
		self.assertEqual(self.CAM["test"], "ok")
		
	def test_iter(self):
		for item in self.CAM:
			with self.subTest(item=item):
				self.assertEqual(item, (item[0], self.CAM[item[0]]))
	
if __name__ == "__main__":
	unittest.main()