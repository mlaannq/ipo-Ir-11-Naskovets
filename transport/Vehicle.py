import uuid

class Vehicle:
    def __init__(self, capacity, current_load=0):
        self.vehicle_id = str(uuid.uuid4())
        try:
            capacity = int(capacity)
        except ValueError:
            raise ValueError("Грузоподъемность должна быть положительным ЧИСЛОМ")
        try:
            current_load = int(current_load)
        except ValueError:
            raise ValueError("Текущая загрузка указывается ЧИСЛОМ")

        self.capacity = capacity
        self.clients_list = []
        self.current_load = current_load

    def load_cargo(self, client):
        try:
            new_weight = self.current_load + client.cargo_weight
        except AttributeError:
            raise AttributeError("Вы должны передать клиента в параметр функции!")

        if new_weight > self.capacity:
            print("Грузоподъемность превышена")
        else:
            self.current_load = new_weight
            self.clients_list.append(client)

    def __str__(self):
        return (f"ID транспорта: {self.vehicle_id}\n"
                f"Грузоподъемность транспорта: {self.capacity}\n"
                f"Загружено: {self.current_load}")

class Train(Vehicle):
    def __init__(self, capacity, number_of_cars):
        if isinstance(number_of_cars, int) and number_of_cars > 0:
            super().__init__(capacity)
            self.number_of_cars = number_of_cars
        else:
            raise ValueError("Кол-во вагонов должно быть положительным числом")

class Airplane(Vehicle):
    def __init__(self, capacity, max_altitude):
        if isinstance(max_altitude, (int, float)) and max_altitude > 0:
            super().__init__(capacity)
            self.max_altitude = max_altitude
        else:
            raise ValueError("Высота полета должна быть положительным числом!")