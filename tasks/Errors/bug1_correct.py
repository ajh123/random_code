from sam_utilities import validated_input

#This program askes the user for 2 numbers as input
#Then we create a variable that stores the sum and one that stores 
#The difference between the bigger of the two numbers and the smaller one
#Finally we print the numbers with an appropriate message

a = validated_input(int, "Please insert the first number") # `n` in imput was `m` + no type casting + enforce int type
b = validated_input(int, "Please insert second number") # no string + no type casting + enforce int type

s = a + b # `b` was wrong case
d = max(a,b) - min(a,b) # min and max were wrong way round, resulting in a negative difference
print(f"The sum is {s}") # `s` was included as a literal character instead the variable
print("The difference is",d) # string started with `'` but ended with `"`
