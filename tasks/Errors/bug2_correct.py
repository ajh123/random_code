# This program tells you how many even numbers are in an array a 
# ^ Missing `#` character

a = [1,4,5,8,10,62,18,54,3] # List started with `{` instead of `[`
count = 0
for i in a: # Missing `:`
    if i % 2 == 0: # Needs to be `==`
        count = count + 1 # Needs to be `=`
print("There are", count, "even numbers in \"a\"") # String was completely none existant
