a, b, c = map(int, input("Введите три числа через пробел: ").split())
min_val = a
if b < min_val:
    min_val = b
if c < min_val:
    min_val = c
print(min_val)