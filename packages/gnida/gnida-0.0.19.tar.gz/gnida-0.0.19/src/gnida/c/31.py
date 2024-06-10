# 31. Реализовать однонаправленный связанный список (реализовать класс для
# элементов списка). Преобразовать строку 'Eeny, meeny, miney, moe; Catch a tiger by
# his toe.' в связный список символов строки и удалить из него все элементы
# содержащие гласные буквы.

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:  # Проверка на пустой список
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def delete(self):
        vowels = 'AaEeIiOoUuYy'
        dummy = Node(0)
        dummy.next = self.head
        current = dummy
        while current.next:
            if current.next.data in vowels:
                current.next = current.next.next
            else:
                current = current.next
        self.head = dummy.next

    def print_list(self):
        current = self.head
        while current:
            print(str(current.data) + " -> ", end=" ")
            current = current.next
        print("None")


linked_list = LinkedList()

input_string = "Eeny, meeny, miney, moe; Catch a tiger by his toe."

for char in input_string:
    linked_list.append(char)

linked_list.delete()

linked_list.print_list()

