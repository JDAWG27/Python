#Purpose:        Find the largest factor pair from the given integer.
#Design Methodology:    Test Driven Design

#Possible Outputs:
#    False:         There are no factors other than 1 and itself, meaning the number is prime.
#    list[int,int]: This is the factor pair, with the smaller one first and the larger one secound.
import math
def check_int(to_check):
    '''
    Determines if the given variable is an int.
    Returns True if it is an int.
    Returns False if it is anything else, specifies if there was no input.
    ''' 
    try:
        to_check_temp = float(to_check)

    except:
        if((to_check == None) or (to_check == '')):
            print()
            print("Exception:   No Input")
            print()
            return None
        elif(type(to_check) != int):
            print()
            print("Exception:   Not an Integer")
            print()
            return None
        else:
            print()
            print("Exception: Unkown")
            print()
            return None
    else:
        if(type(to_check_temp) == float):
            if(to_check_temp.is_integer()):
                to_check = int(to_check_temp)
                return True
            else:
                return False
        return True

def get_input():
    '''
    Get's user input for the function, calls check_input_int().
    Will ensure a valid input is entered before executing rest of program.
    '''
    while True:
        print("Please enter an integer:")
        user_input = input() 
        if(check_int(user_input) == True):
            user_input = int(float(user_input))     ##DOUBLE CAST TO ENABLE STRING->FLOAT->INT
            break

    return(user_input)

def is_prime(num):
    '''
    Determines if the given number is prime
    '''
    if all(num % i != 0 for i in range(2, num)):
        return True
    return False

 
def find_factor(num):
    '''
    Starts at 2 and increases to half of num (rounded).
    When num/i is a whole number, we find that i and the result are the products of num.
    '''
    checked = check_int(num)
    if(checked):
        if(is_prime(num) == True):
            print()
            print("The number is Prime, therefore it has no factors other than 1 and itself.")
            print()
            return False
        for i in range(2,(int(round(num/2)))):
            if(check_int(num/i) == True):
                factor_pair = [i,int(num/i)]
                print()
                print("Largest Factor Pair:")
                print(factor_pair)
                print()
                return factor_pair
    elif(checked == None):
        return None
    return False


'''MAIN'''
find_factor(get_input())
