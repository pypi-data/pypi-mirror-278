# Дано два однонаправленных связных списка. Создать список,
# содержащий элементы общие для двух списковДано два однонаправленных связных списка. Создать список,
# содержащий элементы общие для двух списков
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def display(self):
        elems = []
        current = self.head
        while current:
            elems.append(current.data)
            current = current.next
        return elems

    def print_list(self):
        current = self.head
        while current:
            print(str(current.data) + " -> ", end=" ")
            current = current.next
        print("None")


def find_common_elements(list1, list2):
    common_elements = LinkedList()
    elements = set()

    current1 = list1.head
    while current1:
        elements.add(current1.data)
        current1 = current1.next

    current2 = list2.head
    while current2:
        if current2.data in elements:
            common_elements.append(current2.data)
        current2 = current2.next

    return common_elements



list1 = LinkedList()
list1.append(1)
list1.append(2)
list1.append(3)
list1.append(4)
list1.append(5)

list2 = LinkedList()
list2.append(3)
list2.append(4)
list2.append(5)
list2.append(6)
list2.append(7)

common_list = find_common_elements(list1, list2)

print('Первый список: ')
list1.print_list()
print('Второй список: ')
list2.print_list()
print("Общие элементы:", common_list.display())


