numbers = list(map(int, input("Введите числа через пробел: ").split()))
result = max(numbers) / len(numbers)
print(result)