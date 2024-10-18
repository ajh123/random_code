from typing import List

def check_input(inp_type: type, message: str):
    ok = False
    while not ok:
        try:
            temp = inp_type(input(message))
            ok = True
            return temp
        except ValueError:
            print(f"Please enter a valid {inp_type}")
            return check_input(inp_type, message)
        
def choose_from(items: List[str], items_type: str) -> str:
    print(f"Please choose from one these {items_type}s {items}")
    item = input()
    if item in items:
        return item
    else:
        print(f"{item} is not a valid {items_type}, please try again")
        return choose_from(items, items_type)


num1 = check_input(int, "Enter first number: ")
num2 = check_input(int, "Enter second number: ")
op = choose_from(["+", "-", "*", "/"], "operator")

result = None
if op =="+":
    result = num1 + num2
elif op =="-":
    result = num1 - num2
elif op =="*":
    result = num1 * num2
else:
    result = num1 / num2

print(f"{num1} {op} {num2} = {result}")