from sam_utilities import validated_input
from sam_utilities.maths import is_positive

user_sum = 0
running = True

while running:
    num = validated_input(int, "Enter a number you whish to add to a sum. Or enter 0 to stop. ")
    if num == 0:
        running = False
        break
    if is_positive(num):
        user_sum += num
        print(f"Added {num} to the sum.")
    else:
        print("That number is not positive, try again")

print(f"The result of the sum is {user_sum}")