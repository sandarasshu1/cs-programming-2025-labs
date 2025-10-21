text = input("Введите строку: ")
result = ""
for i, char in enumerate(text, 1):
    result += char + str(i)
print(f"Результат: {result}")