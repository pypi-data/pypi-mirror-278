# Создать класс Plane (самолетов), имеющий атрибуты: название самолета, количество пассажиров на борту, курс движения (откуда и куда).
# Методы:
# - определить загрузку самолета, если максимальная вместимость =200 пассажиров;
# – определить все имена самолетов, летящих по одному маршруту;
# - определить среднюю загрузку всех самолетов.

class Plane:
    MAX_CAPACITY = 200

    def __init__(self, name, passengers, origin, destination):
        self.name = name
        self.passengers = passengers
        self.origin = origin
        self.destination = destination

    def load_factor(self):
        return f"{self.name} загружен на {(self.passengers / Plane.MAX_CAPACITY) * 100}%"


class Fleet:
    def __init__(self):
        self.planes = []

    def add_plane(self, plane):
        self.planes.append(plane)

    def planes_by_route(self):
        route_groups = {}
        for plane in self.planes:
            route = (plane.origin, plane.destination)
            if route not in route_groups:
                route_groups[route] = []
            route_groups[route].append(plane)
        return route_groups

    def print_load_factors_by_route(self):
        route_groups = self.planes_by_route()
        for route, planes in route_groups.items():
            origin, destination = route
            print(f"Маршрут: {origin} -> {destination}")
            for plane in planes:
                print(f"{plane.name}")
            print()

    def average_load_factor(self):
        if not self.planes:
            return 0
        total_load_factor = sum(((plane.passengers / Plane.MAX_CAPACITY) * 100) for plane in self.planes)
        return total_load_factor / len(self.planes)


plane1 = Plane("Boeing 737", 150, "Москва", "Калининград")
plane2 = Plane("Airbus A320", 180, "Москва", "Калининград")
plane3 = Plane("Boeing 777", 200, "Сочи", "Екатеринбург")
plane4 = Plane("Airbus A330", 100, "Москва", "Калининград")
plane5 = Plane("Boeing 787", 30, "Сочи", "Екатеринбург")

fleet = Fleet()
fleet.add_plane(plane1)
fleet.add_plane(plane2)
fleet.add_plane(plane3)
fleet.add_plane(plane4)
fleet.add_plane(plane5)

planes = [plane1, plane2, plane3, plane4, plane5]

print(f"Загрузка самолетов:")
for plane in planes:
    print(plane.load_factor())
print()
fleet.print_load_factors_by_route()
print()
print(f"Средняя загрузка всех самолетов: {fleet.average_load_factor()}%")
