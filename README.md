## Задание 1

**Создать класс `Client` для клиентов компании.**

- Атрибуты:
    - `name` – имя клиента
    - `cargo_weight` – вес груза
    - `is_vip` – флаг VIP-статуса (по умолчанию `False`)

## Задание 2

**Создать базовый класс `Vehicle` для транспортного средства.**

- Атрибуты:
    - `vehicle_id` – уникальный идентификатор (строка, генерируется случайно при создание)
    - `capacity` – грузоподъемность (в тоннах)
    - `current_load` – текущая загрузка (по умолчанию 0)
    - `clients_list` — список клиентов чьи грузы загружены
- Методы:
    - `load_cargo(client)` – увеличивает загрузку на `cargo_weight` из объекта `client` и добавляет клиента в список клиентов (с проверкой на не превышение грузоподъемности и валидацией типов данных)
- Магический метод `__str__`: возвращает строку с ID транспорта, его грузоподъемностью и текущей загрузкой
1. **Создать класс `Train` (поезд), наследующий от `Vehicle`.**
    - Дополнительные атрибуты:
        - `number_of_cars` – количество вагонов,
2. **Создать класс `Airplane` (самолет), наследующий от `Vehicle`.**
    - Дополнительные атрибуты:
        - `max_altitude` – максимальная высота полета (в метрах),
3. **Создать класс `TransportCompany`.**
    - Атрибуты:
        - `name` – название компании,
        - `vehicles` – список транспортных средств (всех),
        - `clients` – список клиентов.
    - Методы:
        - `add_vehicle(vehicle)` – добавляет транспортное средство (с валидацией),
        - `list_vehicles()` – возвращает список всех транспортных средств.
        - `add_client(client)` – добавляет клиента,
        - `optimize_cargo_distribution()` – распределяет грузы клиентов по транспортным средствам. С учетом следующего:
            - Грузы вип клиентов загружаются в первую очередь
            - Для загрузки нужно использовать как можно меньше транспорта
