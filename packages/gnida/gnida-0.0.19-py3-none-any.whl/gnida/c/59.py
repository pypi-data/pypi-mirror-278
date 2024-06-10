# Соединить два однонаправленных связных списка

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def display(self):
        current_node = self.head
        while current_node:
            print(current_node.data, end=" -> ")
            current_node = current_node.next
        print("None")

    def extend(self, other_list):
        if self.head is None:
            self.head = other_list.head
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = other_list.head


list1 = LinkedList()
list1.append(1)
list1.append(2)
list1.append(3)


list2 = LinkedList()
list2.append(4)
list2.append(5)
list2.append(6)


print("Первый список:")
list1.display()
print("Второй список:")
list2.display()


list1.extend(list2)


print("Объединенный список:")
list1.display()
