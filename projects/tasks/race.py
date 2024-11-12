from sam_utils import yes_or_no_input, validated_input

names = []
times = []

adding = True
while adding:
    name = input("Enter the person's name. ")
    finish = validated_input(float, "Enter the person's time in seconds. ")
    names.append(name)
    times.append(finish)

    carry_on = yes_or_no_input("Do you want to add more people?")
    if carry_on == "no":
        adding = False

for i in range(0, len(names)):
    print(f"{names[i]} finished at {times[i]}")