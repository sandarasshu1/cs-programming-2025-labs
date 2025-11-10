purchase = float(input("Введите сумму покупки: "))
if purchase < 1000:
    discount = 0
elif purchase <= 5000:
    discount = 5
elif purchase <= 10000:
    discount = 10
else:
    discount = 15

final_price = purchase * (1 - discount / 100)
print(f"Скидка: {discount}%")
print(f"Итоговая сумма: {final_price:.2f}")