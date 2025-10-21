print("Программа для сложения двух чисел (для выхода нажмите Ctrl+C)")
while True:
    numbers_input = input("Введите 2 числа через пробел: ")
    try:
        num1, num2 = map(int, numbers_input.split())
        sum_result = num1 + num2
        print(f"Сумма равна: {sum_result}")
        print("")
    except ValueError:
        print("Ошибка! Пожалуйста, введите 2 целых числа через пробел.")
    except KeyboardInterrupt:
        print("\nПрограмма завершенна.")
        break