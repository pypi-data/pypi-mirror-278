# 25. Создать класс стек. Использовать способ реализации стека через list.
# Сформировать стек с элементами - строками. Прочитать три нижних элемента
# стека и поменять местами верхний и нижний элементы.

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
            return "Стек пустой"

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return "Стек пустой"

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


def main():
    stack = Stack()
    stack.push("Первый")
    stack.push("Второй")
    stack.push("Третий")
    stack.push("Четвертый")
    stack.push("Пятый")

    print("Последние 3 элемента:", stack.items[(stack.size() - 3):])

    top_element = stack.pop()
    bottom_element = stack.items.pop(0)
    stack.items.insert(0, top_element)
    stack.push(bottom_element)

    print("Стек после смены местами верхнего и нижнего элемента:")
    print(stack)


if __name__ == "__main__":
    main()
