hour = int(input("Введите час (0-23): "))
if 0 <= hour <= 5:
    print("Ночь")
elif 6 <= hour <= 11:
    print("Утро")
elif 12 <= hour <= 17:
    print("День")
else:
    print("Вечер")