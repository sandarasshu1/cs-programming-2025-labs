words = input("Введите слова через пробел: ").split()
result = {}
for word in words:
    first_letter = word[0]
    if first_letter not in result:
        result[first_letter] = []
    result[first_letter].append(word)
print(result)