# Реализовать декоратор с именем print_type, выводящий на печать тип
# значения, возвращаемого декорируемой функцией.

def print_type(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(type(result))
        return result

    return wrapper


@print_type
def my_function(data):
    return data


my_function(1)
my_function('пример')
