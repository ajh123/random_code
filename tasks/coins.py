from sam_utilities import validated_input

coins = [1, 5, 10, 25]

change = validated_input(int, "Enter change. ")
count = [0, 0, 0, 0]
n = len(coins)
for i in range(-1, n):
    while coins[i] <= change:
        change = change - coins[i]
        count[i] = count[i] + 1
    if count[i] > 0:
        print(f"Coin {coins[i]} was used {count[i]} times")
    if change == 0:
        break
