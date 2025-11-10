def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

while True:
    user_input = input("Введите целое число: ")
    if user_input.lstrip('-').isdigit():
        num = int(user_input)
        if num >= 0:
            print("Простое" if is_prime(num) else "Составное")
            break
        else:
            print("Число должно быть неотрицательным.")
    else:
        print("Ошибка: введите целое число.")