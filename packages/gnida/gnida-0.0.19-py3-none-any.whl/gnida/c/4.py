# 4. Создать класс стек. Использовать способ реализации стека через list. Удалить элемент, который находится в
# середине стека, если нечетное число элементов, а если четное, то два средних

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

    def remove_middle(self):
        size = self.size()
        if size == 0:
            return None

        mid_index = size // 2
        if size % 2 == 1:
            del self.items[mid_index]
        else:
            del self.items[mid_index - 1: mid_index + 1]

    def __str__(self):
        return str(self.items)


stack = Stack()
elements = [1, 2, 3, 4, 5, 6]

for elem in elements:
    stack.push(elem)

print("Стек до удаления среднего элемента:", stack)
stack.remove_middle()
print("Стек после удаления среднего элемента:", stack)
