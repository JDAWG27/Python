#Demonstration of For Loop, asks for a number and stores that number, counts up to 100, and counts the difference between the number entered and 100

#Define Variablres
numberstr = input("Please enter a number: ")
numberint = int(numberstr)
print(f"{numberint}, {numberstr}")        #Starting point

for numberint in range(numberint, 101):  #As long as the number entered +count is less than or equal to 100, run this loop
    print(f"int:{numberint}, str:{numberstr}")
    numberint += 1                       #increases numberint, so loop does not run infinitely

numberint -= 1                           #Reduces numberint by 1, so it does not read 101
#109print(f"Iterations: {iteration}")
print(f"Original Number: {numberstr}")
print(f"Final Number: {numberint}")
