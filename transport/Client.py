import re #для ипсользования регулярного выражения
class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        #проверка имени клиента
        if not name or not re.match("[A-Za-z]", name): #шаблон из каких символов может состоять имя клиента (регулярное вырожение)
            raise ValueError("Имя клиента должно содержать только буквы и не должно быть пустым")

        self.name = name  #убираем лишние пробелы
        #проверка веса груза
        if not isinstance(cargo_weight, (int, float)) or cargo_weight < 0:
            raise ValueError("Вес груза должен быть положительным ЧИСЛОМ")
        #проверка vip статуса
        if not isinstance(is_vip, bool):
            raise ValueError("VIP-статус должен быть True или False")
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip
