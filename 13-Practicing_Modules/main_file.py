from modules.math.math_lib import add, sub, mult
from modules.string.str_lib import concat, findLen

print("main_file's __name__ is " + __name__)

print(add(1, 2, 3))
print(sub(5, 1, 2))
print(mult(1, 2, 3))


print("Math added with Lib gives " + concat("Math" + " Lib"))
print("Length of string 'Hello World' is " + str(findLen("Hello World"))) 