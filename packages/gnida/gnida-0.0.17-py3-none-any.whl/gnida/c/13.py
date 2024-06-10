# 13. Создать класс стек. Использовать способ реализации стека через list.
# Удалить минимальный элемент стека.

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return None

    def size(self):
        return len(self.items)

    def remove_min(self):
        if self.is_empty():
            return None

        min_value = min(self.items)
        self.items.remove(min_value)
        return min_value

    def __str__(self):
        return str(self.items)


stack = Stack()
elements = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

for elem in elements:
    stack.push(elem)

print("Стек до удаления минимального элемента:", stack)
min_value = stack.remove_min()
print(f"Минимальный элемент: {min_value}")
print("Стек после удаления минимального элемента:", stack)


