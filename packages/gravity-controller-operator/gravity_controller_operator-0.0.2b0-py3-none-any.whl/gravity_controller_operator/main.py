from abc import ABC, abstractmethod
import datetime


class ControllerSoftDict(ABC):
    my_dict = {}
    map_keys_amount: int = None
    starts_with: int = 0

    def init_dict(self):
        """ Создаем словарь, где ключом будет номер реле,
        а значением: еще один словарь с информацией о реле (состояние и тд)

        :return {0: {'state': None, "changed": datetime.datetime.now()},
        1: {...}, ...}"""
        relays_map = {}
        for i in range(self.map_keys_amount):
            # Начинаем генерировать, первое значение - 0
            if self.starts_with:  # Если номер первого реле НА контроллере > 0
                i += self.starts_with  # Плюсуем номер
            relays_map[i] = {"state": None,
                             "changed": datetime.datetime.now()}
        return relays_map

    def set_point_state_in_dict(self, num, state):
        """ Программно задать состояние реле"""
        self.my_dict[num]["state"] = state
        self.my_dict[num]["changed"] = datetime.datetime.now()


class ControllerPhysOperator(ABC):
    """ В этом классе задаются функции для реального
    взаимодействия с контроллером. На новых контроллерах нужно будет менять
    (предопределять только эти методы),
    потому что вся остальная логика меняться не должна,
    меняются только способ и вид взаимодействия с контроллерами"""
    ip = None
    port = None

    @abstractmethod
    def get_phys_dict(self, *args, **kwargs):
        """ Получить состояние входов или выходов с контроллера.
        Перед возвратом привести в вид словаря,
        где ключ - это номер реле или di, значение - 0 или 1.
        """
        return {}


class ControllerPhysRelayOperator(ControllerPhysOperator, ABC):
    @abstractmethod
    def change_phys_relay_state(self, num, state: bool):
        """ Физически изменить состояние реле (обратиться к контроллеру) """
        return


class ControllerInterface(ControllerSoftDict, ControllerPhysOperator, ABC):
    """ Интерфейс для работы с контроллером.
    В нем происходят работы и со словарем состояний и с реальными состояниями
    физического контроллера """
    name = None

    def update_relays_map(self):
        phys_relays_map = self.get_phys_dict()
        if not self.my_dict:
            return {"error": "Init relays map (init_relays_map) first!"}
        for relay, state in phys_relays_map.items():
            self.set_point_state_in_dict(relay, state)


class RelayControllerInterface(ControllerPhysRelayOperator,
                               ControllerInterface, ABC):
    def change_relay_state(self, num: int, state: bool):
        """ Изменить состояние реле"""
        self.set_point_state_in_dict(num, state)
        return self.change_phys_relay_state(num, state)
