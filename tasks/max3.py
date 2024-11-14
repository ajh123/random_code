from sam_utilities import validated_input

numbers = []
while len(numbers) < 3:
    num = validated_input(int, "Please enter a number. ")
    numbers.append(num)

last_big = 0
for num in numbers:
    if num > last_big:
        last_big = num

print(f"The biggest number is {last_big}")