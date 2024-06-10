# 49. Реализовать двоичное дерево в виде связанных объектов (реализовать
# класс для элементов двоичного дерева) и реализовать симметричную процедуру
# обхода двоичного дерева в виде рекурсивной функции.

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def symmetrical(root):
    if root:
        symmetrical(root.left)
        print(root.data, end=" ")
        symmetrical(root.right)


root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)

print("Симметричный обход:")
symmetrical(root)
