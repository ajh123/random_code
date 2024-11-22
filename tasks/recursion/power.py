from sam_utilities import validated_input

x = validated_input(int, "Enter number x.")
y = validated_input(int, "Enter number y.")

# print(x**y)
# print(x*y)

def do_power(x, y):
    print(x, y)
    return do_power(x, (x * y) - 1)

r = do_power(x, y)
print(r)