print("math_lib's __name__ is " + __name__)

def add(*args):
	'''
	returns sum of the arguments provided
	'''
	return sum(args)

def sub(*args):
	'''
	subtracts from the first argument the rest of the arguments
	'''
	i = args[0]
	for item in args[1:]:
		i = i - item
	return i

def mult(*args):
	'''
	returns the multiplication of the arguments
	'''
	i = args[0]
	for item in args[1:]:
		i *= item
	return i
