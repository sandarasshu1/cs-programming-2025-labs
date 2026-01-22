dictionary = {"apple": "яблоко", "cat": "кот", "house": "дом", "dog": "собака", "book": "книга"}
russian_word = input("Введите русское слово: ")
for eng, rus in dictionary.items():
    if rus == russian_word:
        print(f"Перевод: {eng}")
        break
else:
    print("Слово не найдено")