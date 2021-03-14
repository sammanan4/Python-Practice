'''
unit test script
'''
import unittest
from cap import cap

class TestCap(unittest.TestCase):

	def test_one(self):
		test = 'django'
		result = cap(test)
		self.assertEqual(result, 'Django')

	def test_multiple(self):
		test = 'learning python now'
		result = cap(test)
		self.assertEqual(result, 'Learning python now')

if __name__ == '__main__':
	unittest.main()