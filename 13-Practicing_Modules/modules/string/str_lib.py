print("str_lib's __name__ is " + __name__)

def concat(*args):
	s = ""
	for x in args:
		s += x
	return s

def findLen(arg):
	return len(arg)