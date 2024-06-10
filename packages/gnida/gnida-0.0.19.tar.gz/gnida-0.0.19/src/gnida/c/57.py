# Дан двунаправленный связный список. Удалить n-ый элемент списка.
import random


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_node(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = self.head
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def remove_node(self, n):
        if n == 0:
            if self.head is not None:
                self.head = self.head.next
            else:
                raise ValueError("Список пуст")
        else:
            current = self.head
            for i in range(n - 1):
                current = current.next
            if current.next is not None:
                current.next = current.next.next
                if current.next is None:
                    self.tail = current
            else:
                raise IndexError("Вышли за пределы списка")

    def print_list(self):
        current = self.head
        while current is not None:
            print(current.value, end=" ")
            current = current.next


def main():
    list = LinkedList()
    for i in range(10):
        list.add_node(random.randint(1, 100))
    print('Изначальный список')
    list.print_list()
    print()
    print("После удаления 5-ого элемента")
    list.remove_node(5)
    list.print_list()


if __name__ == "__main__":
    main()
