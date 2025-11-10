def dog_to_human(age):
    if age <= 2:
        return age * 10.5
    else:
        return 21 + (age - 2) * 4

while True:
    user_input = input("Введите возраст собаки: ")
    if user_input.isdigit():
        dog_age = int(user_input)
        if 1 <= dog_age <= 22:
            print(dog_to_human(dog_age))
            break
        else:
            print("Ошибка: возраст должен быть от 1 до 22 лет.")
    else:
        print("Ошибка: введите целое число.")