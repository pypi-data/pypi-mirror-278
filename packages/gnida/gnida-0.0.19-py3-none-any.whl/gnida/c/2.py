# Создать класс стек.
# Использовать способ реализации стека через list.
# Поменять местами первый и последний элементы стека.
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

    def swap_first_last(self):
        if self.size() > 1:
            self.items[0], self.items[-1] = self.items[-1], self.items[0]

stack = Stack()
elements = [1,2,3,4]
for elem in elements:
    stack.push(elem)


print("Стек до смены местами:", stack.items)
stack.swap_first_last()
print("Стек после смены местами:", stack.items)