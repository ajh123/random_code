import random
from sam_utilities.maths import is_prime

nums = list(range(0, 50))
random.shuffle(nums)

prime_count = 0

for num in nums:
    if is_prime(num):
        prime_count += 1

prop = len(nums) / prime_count
print(prop)