"""
This program asks the user for their name and says hello using a procedure
It then asks the suer how they are and replied based on their answer
If the users' answer in is the first array, then they are ok
If it's in the second then they are not doing so well
If it's in the third then they are so-so
Else the program will not understand
The users's reply is first converted to lower case before being compared to the arrays
Finally the program says goodbye
"""

a = ["good", "ok", "well", "very well", "fine", "not bad"]
b = ["not great","not good", "sick", "tired", "not well"]
c = ["meh", "so so", "hanging in there"]




def hello(name): # `def` was `sub`
    print("Hello", name) # Hello needs to be a string


def reply (answer):
    if answer.lower() in a:
        print("That's nice to hear")
    elif answer in b: # Needs to be `elif` + missing `:`
        print("Oh no, that's too bad, but it will get better")
    elif answer in c: # Missing condition
        print("I feel ya bro")
    else: # Missing `:`
        print("Sorry, didn't get that")

ans = input("What is your name? ")
hello(ans) # Variable `name` does not exist, but `ans` does.
ans = input("How are you? ") # Missing closing `)`
reply(ans)
print("Well, goodbye then") # Typo in `print`
