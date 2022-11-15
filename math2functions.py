#Function Calculator Module

#Define Variables
result = 0

#User Input
#try:
#    num1 = int(input("Please enter the first number: "))
#except:
#    print("Please enter a number")

#try:
#    num2 = int(input("Please enter the secound number: "))
#except:
#    print("Please enter a number")

#ope = input("Please enter mathematic operand +, -. * or x, /: ")
#print()


#Define Functions, they also print the full equation.
def addition(num1, num2):
    print(f"{num1} + {num2} = {num1 + num2}")
    return num1 + num2

def subtraction(num1, num2):
    print(f"{num1} - {num2} = {num1 - num2}")
    return num1 - num2

def multiplication(num1, num2):
    print(f"{num1} * {num2} = {num1 * num2}")
    return num1 * num2

def division(num1, num2):
    print(f"{num1} / {num2} = {num1 / num2}")
    return num1 / num2

#COMMENTED OUT FOR includingmath2.py


#Logical statement for operand, and assigns result using the correct function
#if(ope == '+'):
#    result = addition(num1, num2)
#elif(ope == '-'):
#    result = subtraction(num1, num2)
#elif(ope == '*' or ope == 'x'):
#    result = multiplication(num1, num2)
#elif(ope == '/'):
#    result = division(num1, num2)

#Prints result
#print()
#print(f"The result is {result}.")

