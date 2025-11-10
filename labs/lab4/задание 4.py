num = input("Введите число: ")
total = sum(int(digit) for digit in num)
if total % 3 == 0 and int(num[-1]) % 2 == 0:
    print("Делится на 6")
else:
    print("Не делится на 6")