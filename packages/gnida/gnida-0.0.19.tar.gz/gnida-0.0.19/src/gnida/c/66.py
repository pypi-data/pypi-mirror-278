# Описать функцию, которая:
# a) присваивает параметру Е запись из самого левого листа непустого дерева
# Т (лист-вершина, из которого не выходит ни одной ветви);
# b) определяет число вхождений записи Е в дерево Т.

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self, root=None):
        self.root = root

    def find_leftmost_leaf(self):
        current = self.root
        while current.left:
            current = current.left
        return current.value

    def count_occurrences(self, value):
        return self._count_occurrences(self.root, value)

    def _count_occurrences(self, node, value):
        if not node:
            return 0
        count = 1 if node.value == value else 0
        count += self._count_occurrences(node.left, value)
        count += self._count_occurrences(node.right, value)
        return count

root = TreeNode(10)
root.left = TreeNode(5)
root.right = TreeNode(15)
root.left.left = TreeNode(2)
root.left.right = TreeNode(7)
root.left.left.left = TreeNode(5)
root.right.left = TreeNode(12)
root.right.right = TreeNode(20)

tree = BinaryTree(root)

E = tree.find_leftmost_leaf()

occurrences = tree.count_occurrences(E)

print(f"Запись из самого левого листа: {E}")
print(f"Число вхождений записи {E} в дерево: {occurrences}")

