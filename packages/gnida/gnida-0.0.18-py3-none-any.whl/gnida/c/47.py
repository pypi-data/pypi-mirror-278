# Создать класс Профиль местности, который хранит последовательность высот, вычисленных
# через равные промежутки по горизонтали. Методы: наибольшая высота, наименьшая высота,
# перепад высот (наибольший, суммарный), крутизна (тангенс угла наклона; наибольшая, средняя),
# сравнение двух профилей одинаковой длины (по перепаду, по крутизне)


class TerrainProfile:
    def __init__(self, heights):
        self.heights = heights

    def max_height(self):
        return max(self.heights)

    def min_height(self):
        return min(self.heights)

    def max_drop(self):
        return max(self.heights) - min(self.heights)

    def total_drop(self):
        return sum(abs(self.heights[i] - self.heights[i - 1]) for i in range(1, len(self.heights)))

    def max_slope(self):
        return max(abs(self.heights[i] - self.heights[i - 1]) for i in range(1, len(self.heights)))

    def average_slope(self):
        total_slope = sum(abs(self.heights[i] - self.heights[i - 1]) for i in range(1, len(self.heights)))
        return total_slope / (len(self.heights) - 1)

    def compare_by_drop(self, other):
        if len(self.heights) != len(other.heights):
            return None
        return self.max_drop() - other.max_drop()

    def compare_by_slope(self, other):
        if len(self.heights) != len(other.heights):
            return None
        return self.max_slope() - other.max_slope()

    def __eq__(self, other):
        if len(self.heights) != len(other.heights):
            return False
        return self.heights == other.heights

    def __lt__(self, other):
        if len(self.heights) != len(other.heights):
            return False
        return self.max_drop() < other.max_drop()

    def __le__(self, other):
        if len(self.heights) != len(other.heights):
            return False
        return self.max_drop() <= other.max_drop()

    def __gt__(self, other):
        if len(self.heights) != len(other.heights):
            return False
        return self.max_drop() > other.max_drop()

    def __ge__(self, other):
        if len(self.heights) != len(other.heights):
            return False
        return self.max_drop() >= other.max_drop()


profile1 = TerrainProfile([100, 150, 200, 150, 100])
profile2 = TerrainProfile([100, 200, 150, 250, 100])
profile3 = TerrainProfile([100, 150, 200, 150])  # Другой длины

profiles = [profile1, profile2, profile3]

i = 1
for profile in profiles:
    print(f"Profile {i}:")
    print("Наибольшая высота:", profile.max_height())
    print("Наименьшая высота:", profile.min_height())
    print("Наибольший перепад высот:", profile.max_drop())
    print("Суммарный перепад высот:", profile.total_drop())
    print("Наибольшая крутизна:", profile.max_slope())
    print("Средняя крутизна:", profile.average_slope())
    print()
    i += 1

print("Сравнение (профиль 1 vs профиль 2):")
print("Сравнение по перепаду двух профилей:", profile1.compare_by_drop(profile2))
print("Сравнение по крутизне двух профилей:", profile1.compare_by_slope(profile2))

print("Сравнение (профиль 1 vs профиль 3):")
print("Сравнение по перепаду двух профилей:", profile1.compare_by_drop(profile3))
print("Сравнение по крутизне двух профилей:", profile1.compare_by_slope(profile3))

