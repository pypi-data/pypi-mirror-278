# 58. Добавить элемент в начало однонаправленного связного списка.

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add_to_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")


# Пример использования
linked_list = LinkedList()
linked_list.add_to_beginning(3)
linked_list.add_to_beginning(2)
linked_list.add_to_beginning(1)
linked_list.print_list()
