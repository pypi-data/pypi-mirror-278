# 55. Реализовать функцию st_reverse(a_string), которая при помощи стека
# инвертирует строку (меняет порядок букв на обратный). Пример: st_reverse(‘abcd’)
# -> ‘dcba’.

def st_reverse(a_string):
    stack = []

    for char in a_string:
        stack.append(char)

    reversed_string = ''

    while stack:
        reversed_string += stack.pop()

    return reversed_string


print(st_reverse('abcd'))
