print("Задание 1")
name = input("Введите ваше имя: ")
age = input("Введите ваш возраст: ")
for i in range(10):
    print(f"Меня зовут {name} и мне {age} лет")

print("Задание 2")
number = int(input("Введите число от 1 до 9:"))
print(f"Таблица умножения для числа {number}:")
for i in range(1, 11):
    result = number * i
    print(f"{number} * {i} = {result}")