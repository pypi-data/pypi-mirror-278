# Даны 2 списка: перечень товаров и фамилии покупателей.
# Каждый n-й покупатель покупает m-й товар.
# Вывести список покупок

def generate_purchase_list(products, buyers, n, m):
    purchase_list = []
    num_products = len(products)
    num_buyers = len(buyers)

    buyer_index = (n - 1) % num_buyers
    product_index = (m - 1) % num_products

    while buyer_index < num_buyers and product_index < num_products:
        purchase_list.append((buyers[buyer_index], products[product_index]))
        buyer_index += n
        product_index += m

    return purchase_list


products = ["Хлеб", "Молоко", "Сыр", "Масло", "Яйца", "Мясо", "Рыба"]
buyers = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов"]

n = 2
m = 3

purchase_list = generate_purchase_list(products, buyers, n, m)

print("Список покупок:")
for buyer, product in purchase_list:
    print(f"{buyer} покупает {product}")


