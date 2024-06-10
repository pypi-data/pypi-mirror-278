# 34. Описать рекурсивные функции Fact(N) и Fact2(N) вещественного типа,
# вычисляющие значения факториала N! и двойного факториала N!! соответственно
# (N > 0 — параметр целого типа).

def fact(N):
    if N == 1:
        return 1
    else:
        return N * fact(N - 1)


def fact2(N):
    if N == 0 or N == 1:
        return 1
    else:
        return N * fact2(N - 2)


N = int(input('Введите число: '))
print(f"Факториал {N}! = {fact(N)}")
print(f"Двойной факториал {N}!! = {fact2(N)}")



