# Создать класс стек. Использовать способ реализации стека через list.
#  Удалить каждый второй элемент стека.
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def remove_every_second(self):
        temp_stack = Stack()
        while not self.is_empty():
            temp_stack.push(self.pop())
        count = 1
        while not temp_stack.is_empty():
            if count % 2 != 0:
                self.push(temp_stack.pop())
            else:
                temp_stack.pop()
            count += 1

# Пример использования
stack = Stack()
for i in range(1, 11):
    stack.push(i)

print("Исходный стек:", stack.items)

stack.remove_every_second()
print("Стек после удаления каждого второго элемента:", stack.items)
