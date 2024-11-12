list = []

while len(list) < 6:
    string = input("Enter a string you wish to be appened to the list. ")
    print(f"Added {string} to the list.")
    list.append(string)

largest = ""
for ele in list:
    if len(ele) > len(largest):
        largest = ele

print(f"The largest element in the list is {largest}.")