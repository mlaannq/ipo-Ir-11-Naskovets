from .Vehicle import Vehicle
from .Client import Client
class TransportCompany:
    def __init__(self, name):
        if not name or not name.strip():
            raise ValueError("НАПИШИТЕ название компании")
        self.name = name
        self.vehicles = []
        self.clients = []
    def add_vehicle(self, vehicle):
        if isinstance(vehicle, Vehicle):
            self.vehicles.append(vehicle)
    def list_vehicles(self):
        return [str(vehicle) for vehicle in self.vehicles]
    def add_client(self, client):
        if not isinstance(client, Client):
            raise ValueError("Клиентов нет")
        self.clients.append(client)
    def optimize_cargo_distribution(self):
        vip_clients = sorted([client for client in self.clients if client.is_vip], key=lambda client: client.cargo_weight, reverse=True)
        regular_clients = sorted([client for client in self.clients if not client.is_vip], key=lambda client: client.cargo_weight, reverse=True)
        all_clients = vip_clients + regular_clients
        for client in all_clients:
            for vehicle in sorted(self.vehicles, key=lambda vehicle: vehicle.current_load):
                if vehicle.load_cargo(client):
                    continue
    def __str__(self):
        vehicles_info = ', '.join(
            [str(vehicle) for vehicle in self.vehicles])
        return f"Компания: {self.name}, Транспортные средства: [{vehicles_info}]"
