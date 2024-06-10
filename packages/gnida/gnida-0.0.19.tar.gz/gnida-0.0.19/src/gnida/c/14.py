# Задано положительное и отрицательное число в двоичной системе.
# Составить программу вычисления суммы этих чисел, используя функцию
# сложения чисел в двоичной системе счисления. Использовать рекурсию.

def binary_to_decimal(binary_str):
    if binary_str[0] == '-':
        return -int(binary_str[1:], 2)
    return int(binary_str, 2)


def decimal_to_binary(decimal_num):
    if decimal_num < 0:
        return '-' + bin(decimal_num)[3:]
    return bin(decimal_num)[2:]


def add_binary(bin1, bin2):
    num1 = binary_to_decimal(bin1)
    num2 = binary_to_decimal(bin2)

    sum_decimal = num1 + num2

    return decimal_to_binary(sum_decimal)


def recursive_add_binary(bin1, bin2, carry='0'):
    if not bin1 and not bin2 and carry == '0':
        return ''

    a = bin1[-1] if bin1 else '0'
    b = bin2[-1] if bin2 else '0'

    sum_bits = int(a) + int(b) + int(carry)

    new_carry = '1' if sum_bits >= 2 else '0'
    current_bit = str(sum_bits % 2)

    remaining_bin1 = bin1[:-1] if bin1 else ''
    remaining_bin2 = bin2[:-1] if bin2 else ''

    return recursive_add_binary(remaining_bin1, remaining_bin2, new_carry) + current_bit


def add_binary_numbers(bin1, bin2):
    sign = ''
    if bin1[0] == '-' and bin2[0] == '-':
        sign = '-'
        bin1 = bin1[1:]
        bin2 = bin2[1:]
    elif bin1[0] == '-':
        return subtract_binary(bin2, bin1[1:])
    elif bin2[0] == '-':
        return subtract_binary(bin1, bin2[1:])

    result = recursive_add_binary(bin1, bin2)
    return sign + result


def subtract_binary(bin1, bin2):
    num1 = binary_to_decimal(bin1)
    num2 = binary_to_decimal(bin2)

    diff_decimal = num1 - num2

    return decimal_to_binary(diff_decimal)


positive_binary = str(input('Введите положительное число в двоичной системе исчисления: '))
negative_binary = str(input('Введите отрицательное число в двоичной системе исчисления: '))

result = add_binary_numbers(positive_binary, negative_binary)
print(f"Сумма чисел {positive_binary} и {negative_binary} равна {result}")


