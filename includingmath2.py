#Imports another python file, it will be executed the moment the import line is found, can access variables and functions using DOT notation (filename.component name)
import math2functions

#Define Variables, verify num1 and num2
try:
    num1 = int(input("Please enter the first integer to be calculated: "))
except:
    print("Please use an integer.")

try:
    num2 = int(input("Please enter the secound integer to be calculated: "))
except:
    print("Please use an integer.")


ope = input("Please enter mathematic operand +, -. *, /: ")
print()

#Logical Process, and verifies ope variable
#Note: math2functions functions also print the whole equation
if(ope == '+'):
    math2functions.result = math2functions.addition(num1, num2)
elif(ope == '-'):
    math2functions.result = math2functions.subtraction(num1, num2)
elif(ope == '*'):
    math2functions.result = math2functions.multiplication(num1, num2)
elif(ope == '/'):
    math2functions.result = math2functions.division(num1, num2)
else:
    print(f'Exception: Operand "{ope}" not found')

#Prints result without equation
print()
print(f"The result is {math2functions.result}.")
