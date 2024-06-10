# 10. Реализовать декоратор с именем not_none, который генерирует
# исключительную ситуацию если декорируемая функция вернула значения None.

def not_none(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            raise ValueError("Эта функция возвращает None")
        return result
    return wrapper


@not_none
def example_function(x):
    if x > 0:
        return x
    else:
        return None


try:
    print(example_function(5))
    print(example_function(-1))
except ValueError as e:
    print(e)

