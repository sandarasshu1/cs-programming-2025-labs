print("Задание 1")
interger_var = 42
float_var = 3.14
string_war = "Hello world!"
bool_var = True

print(f"int {interger_var}, float: {float_var}, str: '{string_war}', bool: {bool_var}")

print("Задание 2")
name = "Дмитрий"
age = 18
print(f"Имя: {name}")
print(f"Возвраст: {age}")

print("Задание 3")
var1 = 342
var2 = 56.2
var3 = '43'
total_sum = var1 + var2 + int(var3)
print(f"Сумма всех чисел:  {total_sum}")

print("Задание 4")
a = 3
b = 8
result = (a + 4*b) * (a - 3*b) + a**2
print(f"Результат уравнения: {result}")

print("Задание 5")
length = float(input("Введите длину прямоугольника: "))
width = float(input("Введите ширину прямоугольник: "))
area = width*length
perimeter = 2 * (lenght + width)
print(f"Площадь пряиоугольника: {area}")
print(f"Периметр прямоугольника: {perimeter}")

print("Задание 6")
print("*   *   *")
print(" * * * *")
print("    *")

print("Задание 7")
x = 15
y = 4
print("Арифметические операторы:")
print(f"x + y = {x + y}") 
print(f"x - y = {x - y}") 
print(f"x * y = {x * y}") 
print(f"x / y = {x / y}") 
print(f"x // y = {x // y}")
print(f"x % y = {x % y}")
print(f"x * y = {x * y}")
print("Операторы сравнения:")
print(f"x == y: {x == y}")
print(f"x != y: {x != y}")
print(f"x > y: {x > y}")
print(f"x < y: {x < y}")
print(f"x >= y: {x >= y}")
print(f"x <= y: {x <= y}")

print("Задание 8")
my_name = "Дмитрий"
my_age = 18
print(f"Меня зовут {my_name}, мне {age} лет")

print("Задание 9")
sentence = "Съешь ещё этих мягких французских булок, да выпей чаю"
word1 = "Съешь"
word2 = "ещё этих"
word3 = "мягких французских"
word4 = "булок,"
word5 = "да выпей"
word6 = "чаю"
reconstructed_sentence = word1 + " " + word2 + " " + word3 + " " + word4 + " " + word5 + " " + word6
print(f"{reconstructed_sentence}")

print("Задание 10")
phrase = "Нет! Да! "
repeated_phrase = phrase * 4
print(f"{repeated_phrase}")

print("Задание 11")
input_str = input("Введите три числа, разделённых запятой: ")
numbers = input_str.split(',')
a = int(numbers[0].strip())
b = int(numbers[1].strip())
c = int(numbers[2].strip())
result = (a + c) // b 
print(f"Результат уровнения: {result}")

print("Задание 12")
word = input("Введите слово (не менее 10 символов): ")
if len(word) < 10:
    print("Слово должно содержать не менее 10 символов!")
else:
    print(f"Первые 4 символа: {word[:4]}")
    print(f"Последние 2 символа: {word[-2:]}")
    print(f"Символы от 4 до 8: {word[4:8]}")
    print(f"Перевёрнутое слово: {word[::-1]}")