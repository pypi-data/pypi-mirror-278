# Создать класс стек.
# Использовать способ реализации стека через list.
# Найти минимальный элемент стека и вставить после него «0»

class Stack:
    def __init__(self):
        self.items = []

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

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def find_and_insert_after_min(self):
        if self.is_empty():
            return

        # Найти минимальный элемент
        min_value = min(self.items)
        min_index = self.items.index(min_value)

        # Вставить 0 после минимального элемента
        self.items.insert(min_index + 1, 0)


stack = Stack()
elements = [3,1,4,2,5]
for elem in elements:
    stack.push(elem)

print("Стек до вставки '0':", stack.items)
stack.find_and_insert_after_min()
print("Стек после вставки '0':", stack.items)
