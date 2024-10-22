items = {"English_Tea": 1.8, "Latte": 2.2, " Cappuccino ": 2.5}
Total_income = 0

for item in items.keys():
    quantity = int(input(f"How many {item}s have you sold? "))
    Total_income = Total_income + quantity * items[item]

print(f"\nThe income today was £{Total_income:0.2f}")
