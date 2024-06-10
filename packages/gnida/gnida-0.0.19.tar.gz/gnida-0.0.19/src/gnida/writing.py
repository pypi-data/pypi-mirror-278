a = ['X = [-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7]', 'p = Fraction(1, len(X))',
     'Px = [p, p, p, p, p, p, p, p, p, p, p, p, p, p, p, p, p]']


def write_me(name):
    result = '\n'.join(a)
    with open(f"{name}.py", "w+") as my_file:
        my_file.write(result)
    return 'Все получилось'
