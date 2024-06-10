# Создать декоратор tol(len, fill) с параметрами len и fill. Декоратор
# превращает результат декорируемой функции в список состоящий из len
# элементов. Если исходная функция возвращает меньше заданного количества
# элементов, то оставшиеся места заполняются значениями fill, в случае, если
# количество возвращаемых элементов больше len, то хвост последовательности
# отбрасывается

def tol(length, fill):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if len(result) < length:
                result.extend([fill] * (length - len(result)))
            elif len(result) > length:
                result = result[:length]
            return result

        return wrapper

    return decorator


@tol(5, 0)
def example_function():
    return [1, 2, 3]


result = example_function()
print(result)
