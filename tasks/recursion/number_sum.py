from sam_utilities import validated_input

dest_num = validated_input(int, "Enter the destination number.")
# total = 0
# for nun in range(0, dest_num):
#     total += nun

# print(total)

def do_sum(total = 0, curr_num = 0, dest_num = 0):
    if curr_num != dest_num:
        total += curr_num
        curr_num += 1
        total = do_sum(total, curr_num, dest_num)
    return total

total = do_sum(dest_num=dest_num)
print(total)