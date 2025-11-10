password = input("Введите пароль: ")
has_upper = any(c.isupper() for c in password)
has_lower = any(c.islower() for c in password)
has_digit = any(c.isdigit() for c in password)
has_special = any(not c.isalnum() for c in password)

errors = []
if len(password) < 8:
    errors.append("длина менее 8 символов")
if not has_upper:
    errors.append("нет заглавных букв")
if not has_lower:
    errors.append("нет строчных букв")
if not has_digit:
    errors.append("нет цифр")
if not has_special:
    errors.append("нет специальных символов")

if errors:
    print("Пароль ненадежный. Отсутствует:", ", ".join(errors))
else:
    print("Пароль надежный")