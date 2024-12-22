import tkinter as tk
from tkinter import messagebox, ttk
import json
import re

class Client:
    def __init__(self, name, cargo_weight, is_vip):
        self.name = name.strip()
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip

class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.clients = []
        self.vehicles = []

    def add_client(self, client):
        self.clients.append(client)

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle):
        self.vehicles.remove(vehicle)

    def optimize_cargo_distribution(self):
        for client in self.clients:
            distributed = False
            for vehicle in self.vehicles:
                if client.cargo_weight <= vehicle.capacity:
                    distributed = True
                    break
            if not distributed:
                messagebox.showwarning("Предупреждение", f"Груз клиента {client.name} не может быть распределен")

class Airplane:
    def __init__(self, capacity, max_altitude):
        self.capacity = capacity
        self.max_altitude = max_altitude

class Train:
    def __init__(self, capacity, number_of_cars):
        self.capacity = capacity
        self.number_of_cars = number_of_cars

class TransportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Транспортная Компания 'Ветерок'")
        self.root.configure(bg="#FFEFDB")  #бежевый фон
        self.company = TransportCompany("Veterok")
        self.load_data()

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Экспорт результата", command=self.export_results)
        file_menu.add_command(label="О программе", command=self.show_about)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="#ADD8E6")  # Нежно-синий фон
        frame.pack(padx=10, pady=10)

        # Изменение фона таблицы на светло-серый
        self.tree_clients = ttk.Treeview(frame, columns=("Имя", "Вес", "VIP"), show="headings",
                                          style="Treeview")
        self.tree_clients.heading("Имя", text="Имя")
        self.tree_clients.heading("Вес", text="Вес")
        self.tree_clients.heading("VIP", text="VIP")
        self.tree_clients.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree_vehicles = ttk.Treeview(frame, columns=("Тип", "Грузоподъемность"), show="headings",
                                           style="Treeview")
        self.tree_vehicles.heading("Тип", text="Тип")
        self.tree_vehicles.heading("Грузоподъемность", text="Грузоподъемность")
        self.tree_vehicles.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        control_frame = tk.Frame(self.root, bg="#ADD8E6")  # Нежно-синий фон
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Добавить клиента", command=self.open_add_client_window).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Редактировать клиента", command=self.open_edit_client_window).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Удалить клиента", command=self.delete_client).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Добавить транспорт", command=self.open_add_vehicle_window).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Удалить транспорт", command=self.delete_vehicle).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Распределить грузы", command=self.optimize_cargo).pack(side=tk.LEFT, padx=5)

        self.status_bar = tk.Label(self.root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#ADD8E6")  # Нежно-синий фон
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree_clients.bind("<Double-1>", self.open_edit_client_window)
        self.tree_vehicles.bind("<Double-1>", self.open_edit_vehicle_window)

        self.update_clients()
        self.update_vehicles()

        # Создание стиля для таблицы
        style = ttk.Style()
        style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
        style.map("Treeview", background=[("selected", "#A9A9A9")])  # Цвет фона для выделенных строк

    # Остальная часть кода остается без изменений...

    def open_add_client_window(self):
        self.client_window = tk.Toplevel(self.root)
        self.client_window.title("Добавить клиента")
        self.client_window.configure(bg="#ADD8E6")  # Нежно-синий фон

        tk.Label(self.client_window, text="Имя клиента:", bg="#ADD8E6").pack()
        self.client_name_entry = tk.Entry(self.client_window)
        self.client_name_entry.pack()

        tk.Label(self.client_window, text="Вес груза:", bg="#ADD8E6").pack()
        self.client_weight_entry = tk.Entry(self.client_window)
        self.client_weight_entry.pack()

        tk.Label(self.client_window, text="VIP клиент:", bg="#ADD8E6").pack()
        self.client_is_vip_var = tk.BooleanVar()
        tk.Checkbutton(self.client_window, variable=self.client_is_vip_var, bg="#ADD8E6").pack()

        tk.Button(self.client_window, text="Сохранить", command=self.add_client).pack()
        tk.Button(self.client_window, text="Закрыть", command=self.client_window.destroy).pack()

    def open_edit_client_window(self, event=None):
        selected_item = self.tree_clients.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите клиента для редактирования")
            return

        selected_client_id = selected_item[0]
        client_data = self.tree_clients.item(selected_client_id)["values"]

        self.client_window = tk.Toplevel(self.root)
        self.client_window.title("Редактировать клиента")
        self.client_window.configure(bg="#ADD8E6")  # Нежно-синий фон

        tk.Label(self.client_window, text="Имя клиента:", bg="#ADD8E6").pack()
        self.client_name_entry = tk.Entry(self.client_window)
        self.client_name_entry.insert(0, client_data[0])
        self.client_name_entry.pack()

        tk.Label(self.client_window, text="Вес груза:", bg="#ADD8E6").pack()
        self.client_weight_entry = tk.Entry(self.client_window)
        self.client_weight_entry.insert(0, client_data[1])
        self.client_weight_entry.pack()

        tk.Label(self.client_window, text="VIP клиент:", bg="#ADD8E6").pack()
        self.client_is_vip_var = tk.BooleanVar(value=(client_data[2] == "да"))
        tk.Checkbutton(self.client_window, variable=self.client_is_vip_var, bg="#ADD8E6").pack()

        tk.Button(self.client_window, text="Сохранить", command=lambda: self.edit_client(selected_client_id)).pack()
        tk.Button(self.client_window, text="Закрыть", command=self.client_window.destroy).pack()

    def add_client(self):
        name = self.client_name_entry.get()
        if not name or len(name) < 2 or not re.match("^[A-Za-zА-Яа-яЁё]+$", name):
            messagebox.showerror("Ошибка", "Имя клиента должно содержать только буквы и быть не менее 2 символов")
            return

        try:
            weight = float(self.client_weight_entry.get())
            if weight <= 0 or weight > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Вес груза должен быть положительным числом не более 10 тонн")
            return

        is_vip = self.client_is_vip_var.get()
        client = Client(name, weight, is_vip)
        self.company.add_client(client)
        self.update_clients()
        self.export_results()
        self.client_window.destroy()

    def edit_client(self, selected_client_id):
        name = self.client_name_entry.get()
        if not name or len(name) < 2 or not re.match("^[A-Za-zА-Яа-яЁё]+$", name):
            messagebox.showerror("Ошибка", "Имя клиента должно содержать только буквы и быть не менее 2 символов")
            return

        try:
            weight = float(self.client_weight_entry.get())
            if weight <= 0 or weight > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Вес груза должен быть положительным числом не более 10 тонн")
            return

        is_vip = self.client_is_vip_var.get()
        client_index = self.tree_clients.index(selected_client_id)
        client = self.company.clients[client_index]
        client.name = name
        client.cargo_weight = weight
        client.is_vip = is_vip

        self.update_clients()
        self.export_results()
        self.client_window.destroy()

    def delete_client(self):
        selected_item = self.tree_clients.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите клиента для удаления")
            return
        confirm = messagebox.askyesno("Подтверждение удаления", "Вы уверены, что хотите удалить этого клиента?")
        if confirm:
            selected_client_id = selected_item[0]
            client_data = self.tree_clients.item(selected_client_id)["values"]
            client_name = client_data[0]
            self.company.clients = [client for client in self.company.clients if client.name != client_name]
            self.update_clients()
            self.export_results()

    def open_add_vehicle_window(self):
        self.vehicle_window = tk.Toplevel(self.root)
        self.vehicle_window.title("Добавить транспорт")
        self.vehicle_window.configure(bg="#ADD8E6")  # Нежно-синий фон

        tk.Label(self.vehicle_window, text="Тип транспорта\n(самолет/поезд):", bg="#ADD8E6").pack()
        self.vehicle_type_entry = tk.Entry(self.vehicle_window)
        self.vehicle_type_entry.pack()

        tk.Label(self.vehicle_window, text="Грузоподъемность:", bg="#ADD8E6").pack()
        self.vehicle_capacity_entry = tk.Entry(self.vehicle_window)
        self.vehicle_capacity_entry.pack()

        tk.Label(self.vehicle_window, text="Максимальная высота (если самолет):", bg="#ADD8E6").pack()
        self.max_altitude_entry = tk.Entry(self.vehicle_window)
        self.max_altitude_entry.pack()
        self.max_altitude_entry.config(state='disabled')  # Отключаем по умолчанию

        tk.Label(self.vehicle_window, text="Количество вагонов (если поезд):", bg="#ADD8E6").pack()
        self.number_of_cars_entry = tk.Entry(self.vehicle_window)
        self.number_of_cars_entry.pack()
        self.number_of_cars_entry.config(state='disabled')  # Отключаем по умолчанию

        self.vehicle_type_entry.bind("<KeyRelease>", self.update_vehicle_fields_state)

        tk.Button(self.vehicle_window, text="Сохранить", command=self.add_vehicle).pack()
        tk.Button(self.vehicle_window, text="Закрыть", command=self.vehicle_window.destroy).pack()

    def update_vehicle_fields_state(self, event):
        vehicle_type = self.vehicle_type_entry.get().strip().lower()
        if vehicle_type == "самолет":
            self.max_altitude_entry.config(state='normal')  # Включаем поле для высоты
            self.number_of_cars_entry.config(state='disabled')  # Отключаем поле для вагонов
        elif vehicle_type == "поезд":
            self.max_altitude_entry.config(state='disabled')  # Отключаем поле для высоты
            self.number_of_cars_entry.config(state='normal')  # Включаем поле для вагонов
        else:
            self.max_altitude_entry.config(state='disabled')  # Отключаем поле для высоты
            self.number_of_cars_entry.config(state='disabled')  # Отключаем поле для вагонов

    def open_edit_vehicle_window(self, event=None):
        selected_item = self.tree_vehicles.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите транспорт для редактирования")
            return

        selected_vehicle_id = selected_item[0]
        vehicle_data = self.tree_vehicles.item(selected_vehicle_id)["values"]

        self.vehicle_window = tk.Toplevel(self.root)
        self.vehicle_window.title("Редактировать транспорт")
        self.vehicle_window.configure(bg="#ADD8E6")  # Нежно-синий фон

        tk.Label(self.vehicle_window, text="Тип транспорта\n(самолет/поезд):", bg="#ADD8E6").pack()
        self.vehicle_type_entry = tk.Entry(self.vehicle_window)
        self.vehicle_type_entry.insert(0, vehicle_data[0])
        self.vehicle_type_entry.pack()

        tk.Label(self.vehicle_window, text="Грузоподъемность:", bg="#ADD8E6").pack()
        self.vehicle_capacity_entry = tk.Entry(self.vehicle_window)
        self.vehicle_capacity_entry.insert(0, vehicle_data[1])
        self.vehicle_capacity_entry.pack()

        tk.Label(self.vehicle_window, text="Максимальная высота (если самолет):", bg="#ADD8E6").pack()
        self.max_altitude_entry = tk.Entry(self.vehicle_window)
        if vehicle_data[0].lower() == "самолет":
            self.max_altitude_entry.insert(0, "10000")
            self.max_altitude_entry.config(state='normal')
        else:
            self.max_altitude_entry.config(state='disabled')

        tk.Label(self.vehicle_window, text="Количество вагонов (если поезд):", bg="#ADD8E6").pack()
        self.number_of_cars_entry = tk.Entry(self.vehicle_window)
        if vehicle_data[0].lower() == "поезд":
            self.number_of_cars_entry.insert(0, "10")
            self.number_of_cars_entry.config(state='normal')
        else:
            self.number_of_cars_entry.config(state='disabled')

        self.vehicle_type_entry.bind("<KeyRelease>", self.update_vehicle_fields_state)

        tk.Button(self.vehicle_window, text="Сохранить", command=lambda: self.edit_vehicle(selected_vehicle_id)).pack()
        tk.Button(self.vehicle_window, text="Закрыть", command=self.vehicle_window.destroy).pack()

    def add_vehicle(self):
        vehicle_type = self.vehicle_type_entry.get().strip().lower()
        if vehicle_type not in ["самолет", "поезд"]:
            messagebox.showerror("Ошибка", "Введен неправильный тип транспорта")
            return
        try:
            capacity = float(self.vehicle_capacity_entry.get())
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Грузоподъемность должна быть положительным числом")
            return
        if vehicle_type == "самолет":
            try:
                max_altitude = float(self.max_altitude_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Максимальная высота должна быть числом")
                return
            vehicle = Airplane(capacity, max_altitude)
        elif vehicle_type == "поезд":
            try:
                number_of_cars = int(self.number_of_cars_entry.get())
                if number_of_cars <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Количество вагонов должно быть положительным целым числом")
                return
            vehicle = Train(capacity, number_of_cars)

        self.company.add_vehicle(vehicle)
        self.update_vehicles()
        self.export_results()
        self.vehicle_window.destroy()

    def edit_vehicle(self, selected_vehicle_id):
        vehicle_type = self.vehicle_type_entry.get().strip().lower()
        if vehicle_type not in ["самолет", "поезд"]:
            messagebox.showerror("Ошибка", "Введен неправильный тип транспорта")
            return
        try:
            capacity = float(self.vehicle_capacity_entry.get())
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Грузоподъемность должна быть положительным числом")
            return

        vehicle_index = self.tree_vehicles.index(selected_vehicle_id)
        if vehicle_type == "самолет":
            try:
                max_altitude = float(self.max_altitude_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Максимальная высота должна быть числом")
                return
            vehicle = Airplane(capacity, max_altitude)
        elif vehicle_type == "поезд":
            try:
                number_of_cars = int(self.number_of_cars_entry.get())
                if number_of_cars <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Количество вагонов должно быть положительным целым числом")
                return
            vehicle = Train(capacity, number_of_cars)

        self.company.vehicles[vehicle_index] = vehicle
        self.update_vehicles()
        self.export_results()
        self.vehicle_window.destroy()

    def delete_vehicle(self):
        selected_item = self.tree_vehicles.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите транспорт для удаления")
            return

        confirm = messagebox.askyesno("Подтверждение удаления транспорта",
                                       "Вы уверены, что хотите удалить этот транспорт?")
        if confirm:
            selected_vehicle_id = selected_item[0]
            vehicle_index = self.tree_vehicles.index(selected_vehicle_id)
            del self.company.vehicles[vehicle_index]
            self.update_vehicles()
            self.export_results()

    def update_clients(self):
        for row in self.tree_clients.get_children():
            self.tree_clients.delete(row)
        for client in self.company.clients:
            self.tree_clients.insert("", "end",
                                     values=(client.name, client.cargo_weight, "да" if client.is_vip else "нет"))

    def update_vehicles(self):
        for row in self.tree_vehicles.get_children():
            self.tree_vehicles.delete(row)
        for vehicle in self.company.vehicles:
            if isinstance(vehicle, Airplane):
                self.tree_vehicles.insert("", "end", values=("Самолет", vehicle.capacity))
            elif isinstance(vehicle, Train):
                self.tree_vehicles.insert("", "end", values=("Поезд", vehicle.capacity))

    def optimize_cargo(self):
        self.company.optimize_cargo_distribution()
        self.status_bar.config(text="Грузы успешно распределены")

    def show_about(self):
        messagebox.showinfo("О программе: " "Транспортная Компания Ветерок",
                            "Лабораторная работа 12\nВариант: 5\nРазработчик: Насковец Милана")

    def export_results(self):
        results = {
            "clients": [{"name": client.name, "weight": client.cargo_weight, "vip": client.is_vip} for client in
                        self.company.clients],
            "vehicles": [{"type": type(vehicle).__name__, "capacity": vehicle.capacity} for vehicle in
                         self.company.vehicles]}
        with open("transport_results.json", "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Экспорт результатов", "Результат успешно экспортирован")

    def load_data(self):
        try:
            with open("transport_results.json", "r") as f:
                data = json.load(f)
                for client_data in data.get("clients", []):
                    client = Client(client_data["name"], client_data["weight"], client_data["vip"])
                    self.company.add_client(client)
                for vehicle_data in data.get("vehicles", []):
                    if vehicle_data["type"] == "Airplane":
                        vehicle = Airplane(vehicle_data["capacity"], 10000)
                    elif vehicle_data["type"] == "Train":
                        vehicle = Train(vehicle_data["capacity"], 10)
                    else:
                        continue
                    self.company.add_vehicle(vehicle)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TransportApp(root)
    root.mainloop()
