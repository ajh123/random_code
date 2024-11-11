from sam_utils import validated_input

# Retreive an input and validate it agasint all integers
destination = validated_input(int, "Enter a number to find its factorial ", "That value is not number, try again")

# By default start at 1
result = 1
# Keep tracp of the sum, so we can display to the user
display_sum = "1"
# Create a loop starting at 2 and ending at destination + 1
for i in range(2, destination + 1):
    # Multiply the current result by the index of the loop
    result = result * i
    # Add the opertation to the sum
    display_sum += f" * {i}"

print(f"The result of {display_sum} is {result}")