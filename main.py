from transport import Client, TransportCompany, Train, Airplane

def menu():
    company = TransportCompany("Veterok")

    while True:
        print("--------------Меню--------------")
        print("1. Добавить клиента")
        print("2. Добавить транспортное средство")
        print("3. Показать все транспортные средства")
        print("4. Показать всех клиентов")
        print("5. Распределить грузы")
        print("6. Удалить клиента")
        print("7. Выйти из программы")

        choice = input("Выберите пункт из предложенного списка: ")

        if choice == "1":
            name = input("Введите имя клиента: ")
            weight = float(input("Введите вес груза в тоннах: "))
            is_vip_str = input("Это VIP клиент? (Да/Нет): ").strip().lower()
            is_vip = True if is_vip_str == 'да' else False
            company.add_client(Client(name, weight, is_vip))
            print("Клиент добавлен!")

        elif choice == "2":
            choice_type_vehicle = input("Выберите вид транспорта (самолет - 1, поезд - 2): ")
            capacity = float(input("Введите грузоподъёмность: "))
            if choice_type_vehicle == "1":
                max_altitude = float(input("Введите максимальную высоту полета: "))
                company.add_vehicle(Airplane(capacity, max_altitude))
                print("Самолет добавлен!")
            elif choice_type_vehicle == "2":
                number_of_cars = int(input("Введите количество вагонов: "))
                company.add_vehicle(Train(capacity, number_of_cars))
                print("Поезд добавлен!")
            else:
                print("Введен неправильный тип транспорта")

        elif choice == "3":
            print("\nТранспортные средства:")
            vehicles = company.list_vehicles()
            if vehicles:
                for vehicle in vehicles:
                    print(vehicle)
            else:
                print("Нет транспортных средств!")

        elif choice == "4":
            print("\nКлиенты:")
            clients = company.list_clients()
            if clients:
                for client in clients:
                    print(f"Имя: {client.name}, Груз: {client.cargo_weight} тонн, VIP: {'да' if client.is_vip else 'нет'}")
            else:
                print("Нет клиентов!")

        elif choice == "5":
            company.optimize_cargo_distribution()
            print("\nГрузы успешно распределены!")
            print("\nРезультат распределения груза:")
            for vehicle in company.vehicles:
                print(vehicle)
                for client in vehicle.clients_list:
                    print(f" - {client.name}: {client.cargo_weight} тонн, VIP: {'да' if client.is_vip else 'нет'}")

        elif choice == "6":
            find_to_deleteclient = input("Введите имя клиента для удаления: ")
            client_found = False
            for client in company.clients:
                if client.name == find_to_deleteclient:
                    company.clients.remove(client)
                    print("Клиент успешно удален")
                    client_found = True
                    break
            if not client_found:
                print("Клиента с таким именем не существует")

        elif choice == "7":
            print("Выход из программы")
            break

        else:
            print("Выберите из раздела меню пункт от 1 до 7")

if __name__ == "__main__":
    menu()
