from sam_utilities import validated_input


ok = False


while not ok:
    reg = input("Enter registration number. ")
    start_hour = validated_input(int, "Enter the hour you start. ")
    end_hour = validated_input(int, "Enter the hour you end. ")

    if len(reg) < 1:
        print("Your registration number is too small")
    elif end_hour < start_hour:
        print("You cannot end before you start.")
    else:
        ok = True

num_hours = end_hour - start_hour

if num_hours <= 1:
    print("No fee to pay")
else:
    price = 1.5 * num_hours
    print(f"Please pay £{price}")