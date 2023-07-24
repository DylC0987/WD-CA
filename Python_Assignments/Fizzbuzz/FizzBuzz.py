# FizzBuzz.py
# Dylan Creedon
# 122117537


# ask the user for input
# a_number = int(input("Enter a number: "))

#check if the number is multiples of 3 - modulus operator
#print "Fizz"
# if a_number % 3 == 0:
# print("Fizz")

# multiples 5
# print "Buzz"

# Multiples of both
#print "FizzBuzz"
# elif a_number % 3 and 5 == 0:
# print("FizzBuzz")
#Otherwise 
#print the number

def FizzBuzz(n):
    if a_number % 3 == 0 and a_number % 5 == 0:
        print("FizzBuzz")
    elif a_number % 5 == 0:
        print("Buzz")
    elif a_number % 3 == 0:
        print("Fizz")
    else:
        print(a_number)    
        

a_number = int(input("Enter a number: "))
FizzBuzz(a_number)

