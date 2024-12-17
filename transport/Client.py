class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        if name:
            self.name = name
        else:
            raise ValueError("Имя клиента должно быть указано")
        if not isinstance(cargo_weight, (int, float)) or cargo_weight < 0:
            raise ValueError("Вес груза должен быть положительным ЧИСЛОМ")
        if not (is_vip == True or is_vip == False):
            raise ValueError("VIP-статус должен быть True или False")
        self.is_vip = bool(is_vip); self.name = name.strip(); self.cargo_weight = cargo_weight; self.is_vip = is_vip


def lient():
    return None