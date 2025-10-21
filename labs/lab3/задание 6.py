limit = int(input("Введите предел для чисел Фибоначчи: "))
a, b = 0, 1
print("Числа Фибоначчи:")
while a <= limit:
    print(a, end=" ")
    a, b = b, a + b