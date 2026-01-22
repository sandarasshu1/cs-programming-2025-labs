def sort_tuple(t):
    if all(type(x) in (int, float) for x in t):
        return tuple(sorted(t))
    return t
user_input = input("Введите элементы кортежа через пробел: ").split()
tuple_data = []
for item in user_input:
    try:
        tuple_data.append(int(item))
    except:
        try:
            tuple_data.append(float(item))
        except:
            tuple_data.append(item)
print(sort_tuple(tuple(tuple_data)))