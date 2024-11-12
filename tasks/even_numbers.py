from sam_utilities.maths import is_numeric, is_even


l = ["fdfdgfd", 432354, 12, 6000, 47437437922121, print, -1, 1.0, (1, 4, 5), "aasafdfdf", int, 6.6]

out = []

for ele in l:
    if is_numeric(ele):
        if is_even(ele):
            out.append(ele)

print(out)