# Описать рекурсивную функцию Root (а, b, ε), которая методом
# деления отрезка пополам находит с точностью ε корень уравнения
# f(x) = 0 на отрезке [а, b] (считать, что ε > 0, а < b,
# f(a) – f(b) < 0 и f(x) — непрерывная и монотонная на отрезке [а, b] функция).


def f(x):
    return x**3 - x - 2  # пример функции

def Root(a, b, epsilon):
    if f(a) * f(b) >= 0:
        raise ValueError("Значения функции в конечных точках должны быть противоположных знаков.")


    def bisection(a, b, epsilon):
        mid = (a + b) / 2
        if abs(f(mid)) < epsilon or (b - a) / 2 < epsilon:
            return mid
        elif f(mid) * f(a) < 0:
            return bisection(a, mid, epsilon)
        else:
            return bisection(mid, b, epsilon)

    return bisection(a, b, epsilon)


a = 1
b = 2
epsilon = 2
root = Root(a, b, epsilon)
print(f"Корень уравнения f(x) = 0 на отрезке [{a}, {b}] с точностью {epsilon} равен {round(root, 10)}")
