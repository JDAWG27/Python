#Simple Calculator Module

#Define Variables via user input
try:
    num1 = int(input("Please enter the first number: "))
except:
    print("Please enter a number")

try:
    num2 = int(input("Please enter the secound number: "))
except:
    print("Please enter a number")



ope = input("Please enter mathematic operand +, -. * or x, /: ")
if(ope == '+'):
    print(f"{num1} + {num2} = {num1 + num2}")
elif(ope == '-'):
    print(f"{num1} - {num2} = {num1 - num2}")
elif(ope == '*' or ope == 'x'):
    print(f"{num1} * {num2} = {num1 * num2}")
elif(ope == '/'):
    print(f"{num1} / {num2} = {num1 / num2}")
else:
    print("Operator not selected")
