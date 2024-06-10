# 19. Дан кольцевой список с перечнем товаров. Выбрать все товары,
# изготовленные фирмой Bosh и создать из них новый список.

class CircularList:
    def __init__(self, items):
        self.items = items

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if not self.items:
            raise StopIteration
        item = self.items[self.index % len(self.items)]
        self.index += 1
        return item

    def to_list(self, count):
        return [self.items[i % len(self.items)] for i in range(count)]


def filter_bosh_products(circular_list):
    return list(filter(lambda product: 'Bosh' in product, circular_list))


def main():
    circular_list = CircularList([
        'Bosh TV', 'Samsung Phone', 'Bosh Fridge', 'LG Monitor', 'Bosh Washing Machine', 'Panasonic Microwave'
    ])

    print("Исходный кольцевой список товаров:")
    print(circular_list.to_list(len(circular_list.items)))

    bosh_products = filter_bosh_products(circular_list.to_list(len(circular_list.items)))

    print("Товары фирмы Bosh:")
    print(bosh_products)


if __name__ == "__main__":
    main()
