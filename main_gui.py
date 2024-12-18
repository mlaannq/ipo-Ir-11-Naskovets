import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json

class Client:
    def __init__(self, name, cargo_weight, is_vip):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip

class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.clients = []
        self.vehicles = []

    def add_client(self, client): #добавляем клиентов и транспортные средства в списки
        self.clients.append(client)

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def optimize_cargo_distribution(self):
        pass

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
        self.company = TransportCompany("Veterok")
        self.load_data()

        self.create_menu()
        self.create_widgets()

    def create_menu(self): #создаем главное окно
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Экспорт результата", command=self.export_results)
        file_menu.add_command(label="О программе", command=self.show_about)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

    def create_widgets(self): #создаем меню
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        self.tree_clients = ttk.Treeview(frame, columns=("Имя", "Вес", "VIP"), show="headings") #отображаем
        self.tree_clients.heading("Имя", text="Имя")
        self.tree_clients.heading("Вес", text="Вес")
        self.tree_clients.heading("VIP", text="VIP")
        self.tree_clients.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree_vehicles = ttk.Treeview(frame, columns=("Тип", "Грузоподъёмность"), show="headings")
        self.tree_vehicles.heading("Тип", text="Тип")
        self.tree_vehicles.heading("Грузоподъёмность", text="Грузоподъёмность")
        self.tree_vehicles.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        #кнопки управления
        tk.Button(control_frame, text="Добавить клиента", command=self.add_client).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Редактировать клиента", command=self.edit_client).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Удалить клиента", command=self.delete_client).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Добавить транспорт", command=self.add_vehicle).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Распределить грузы", command=self.optimize_cargo).pack(side=tk.LEFT, padx=5)

        self.status_bar = tk.Label(self.root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        #отображает сообщения
        self.tree_clients.bind("<Double-1>", self.on_double_click_client)
        #дабл клик для редактирования
        self.update_clients()
        self.update_vehicles()

    def add_client(self): #добавляем клиента
        name = simpledialog.askstring("Имя клиента", "Введите имя клиента:")
        if not name or len(name) < 2:
            messagebox.showerror("Ошибка", "Имя клиента должно быть не менее 2 символов.")
            return

        weight = simpledialog.askfloat("Вес груза", "Введите вес груза в тоннах:")
        if weight is None or weight <= 0 or weight > 10:
            messagebox.showerror("Ошибка", "Вес груза должен быть положительным числом не более 10 тонн.")
            return

        is_vip = messagebox.askyesno("VIP клиент", "Это VIP клиент?")

        client = Client(name, weight, is_vip)
        self.company.add_client(client)
        self.update_clients()
        self.export_results() #сохраняем изменения после добавления

    def edit_client(self):
        selected_item = self.tree_clients.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите клиента для редактирования.")
            return

        selected_client_id = selected_item[0]
        client_data = self.tree_clients.item(selected_client_id)["values"]
        client_index = self.tree_clients.index(selected_client_id)

        name = simpledialog.askstring("Редактировать имя клиента", "Введите новое имя клиента:",
                                       initialvalue=client_data[0])
        #запрашиваем новое имя кллиента
        if not name or len(name) < 2:
            messagebox.showerror("Ошибка", "Имя клиента должно быть не менее 2 символов.")
            return

        weight = simpledialog.askfloat("Редактировать вес груза", "Введите новый вес груза в тоннах:",
                                        initialvalue=client_data[1])
        #запрашиваем новый вес груза
        if weight is None or weight <= 0 or weight > 10:
            messagebox.showerror("Ошибка", "Вес груза должен быть положительным числом не более 10 тонн.")
            return

        is_vip = messagebox.askyesno("VIP клиент", "Это VIP клиент?")
        #обнавляем данные
        client = self.company.clients[client_index]
        client.name = name
        client.cargo_weight = weight
        client.is_vip = is_vip

        self.update_clients()
        self.export_results()  #сохраняем изменения после редактирования

    def delete_client(self):
        selected_item = self.tree_clients.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите клиента для удаления.")
            return

        confirm = messagebox.askyesno("Подтверждение удаления", "Вы уверены, что хотите удалить этого клиента?")
        if confirm:
            selected_client_id = selected_item[0]
            client_index = self.tree_clients.index(selected_client_id)
            del self.company.clients[client_index]
            self.update_clients()
            self.export_results()
    #редактирование с помощью дабл клика
    def on_double_click_client(self, event):
        self.edit_client()
    #добавлем транспорт
    def add_vehicle(self):
        vehicle_type = simpledialog.askstring("Тип транспорта", "Выберите вид транспорта (самолет или поезд):")
        if vehicle_type not in ["самолет", "поезд"]:
            messagebox.showerror("Ошибка", "Введен неправильный тип транспорта")
            return

        capacity = simpledialog.askfloat("Грузоподъёмность", "Введите грузоподъёмность:")
        if capacity is None or capacity <= 0:
            messagebox.showerror("Ошибка", "Грузоподъёмность должна быть положительным числом.")
            return

        if vehicle_type == "самолет":
            max_altitude = simpledialog.askfloat("Максимальная высота полета", "Введите максимальную высоту полета:")
            vehicle = Airplane(capacity, max_altitude)
        elif vehicle_type == "поезд":
            number_of_cars = simpledialog.askinteger("Количество вагонов", "Введите количество вагонов:")
            if number_of_cars is None or number_of_cars <= 0:
                messagebox.showerror("Ошибка", "Количество вагонов должно быть положительным числом.")
                return
            vehicle = Train(capacity, number_of_cars)

        self.company.add_vehicle(vehicle)
        self.update_vehicles()
        self.export_results()
    #обновление списка клиентов
    def update_clients(self):
        for row in self.tree_clients.get_children():
            self.tree_clients.delete(row)
        for client in self.company.clients:
            self.tree_clients.insert("", "end",
                                     values=(client.name, client.cargo_weight, "да" if client.is_vip else "нет"))
    #обновление транспорта
    def update_vehicles(self):
        for row in self.tree_vehicles.get_children():
            self.tree_vehicles.delete(row)
        for vehicle in self.company.vehicles:
            self.tree_vehicles.insert("", "end", values=(type(vehicle).__name__, vehicle.capacity))

    def optimize_cargo(self):
        self.company.optimize_cargo_distribution()
        self.status_bar.config(text="Грузы успешно распределены!")

    def show_about(self): #отображение информации о программе
        messagebox.showinfo("О программе: " "Транспортная Компания Ветерок", "Лабораторная работа 12\nВариант:5 N/A\nРазработчик: Насковец Милана")
    #экспорт данных в json
    def export_results(self):
        results = {
            "clients": [{"name": client.name, "weight": client.cargo_weight, "vip": client.is_vip} for client in self.company.clients],
            "vehicles": [{"type": type(vehicle).__name__, "capacity": vehicle.capacity} for vehicle in self.company.vehicles]
        }
        with open("transport_results.json", "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Экспорт", "Результаты успешно экспортированы в transport_results.json")

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
                    self.company.add_vehicle(vehicle)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TransportApp(root)
    root.mainloop()