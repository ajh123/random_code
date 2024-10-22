items = {“English_Tea": 1.8, “Latte": 2.2, " Cappuccino ": 2.5}
for item in items.keys()
Total_income = 0
quantity = input(f"How many {item}s have you sold? ")
Total_income = Total_income + quantity * items[item]
print(f"\nThe income today was £{income:0.2f}")

## Errors:
# Line 1: use wrong quote for string
# Line 2: does not have a : at the end
# Lines 3 - 5: no indentation
# Line 3: `Total_income` should be before the for loop
# Line 4: you are not converting the input to an integer
# Line 5: you are using the variable `income` instead of Total_income`