print("Задание 2")
number = int(input("Введите число от 1 до 9:"))
print(f"Таблица умножения для числа {number}:")
for i in range(1, 11):
    result = number * i
    print(f"{number} * {i} = {result}")