products = {}
n = int(input("Сколько товаров? "))
for i in range(n):
    name = input("Название товара: ")
    price = int(input("Цена: "))
    products[name] = price
min_product = min(products, key=products.get)
max_product = max(products, key=products.get)
print(f"Минимальная цена: {min_product} - {products[min_product]}")
print(f"Максимальная цена: {max_product} - {products[max_product]}")