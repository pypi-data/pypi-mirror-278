# Создать класс стек. Использовать способ реализации стека через list.
# Удалить каждый второй элемент стека.

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if len(self.items) > 0:
            return self.items.pop()
        else:
            raise IndexError("Стек пуст")

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)

    def is_empty(self):
        return self.size() == 0

    def clear(self):
        self.items.clear()

    def remove_every_other_item(self):
        for i in range(0, len(self.items), 2):
            self.items.pop()


stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)
stack.push(4)
stack.push(5)

print("Размер стека:", stack.size())
print("Элементы стека:", stack.items)

stack.remove_every_other_item()

print("Размер стека после удаления элементов:", stack.size())
print("Элементы стека после удаления:", stack.items)
