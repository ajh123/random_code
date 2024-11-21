from sam_utilities import validate_list_input

numbers = {}

with open("phonebook.txt") as f:
    lines = f.readlines()
    for line in lines:
        data = line.strip().split(",")
        name = data[0]
        number = data[1]
        numbers[name] = number

running = True

while running:
    chocies = list(numbers.keys())
    chocies.append("0")
    for name in numbers:
        print(f"- {name}") 
    
    name = validate_list_input(chocies, "Please choose a name, or 0 to exit. ")
    if name == "0":
        running = False
        break
    print(f"{name}'s phone number is {numbers[name]}")