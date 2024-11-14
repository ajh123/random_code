count = {}

with open("words.txt") as file:
    content = file.read()
    words = content.split(" ")
    for word in words:
        if word.upper() not in count:
            count[word.upper()] = 1
        else:
            count[word.upper()] += 1

print(count)