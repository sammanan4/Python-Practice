def cap(string):
	'''
	returns capitalized string
	'''
	try:
		return string.capitalize()
	except TypeError:
		print('Invalid Operand type')