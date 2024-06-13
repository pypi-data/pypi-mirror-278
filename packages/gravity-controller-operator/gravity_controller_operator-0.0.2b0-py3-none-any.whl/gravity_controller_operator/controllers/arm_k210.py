from gravity_controller_operator.main import ControllerInterface
from pyModbusTCP.client import ModbusClient
from abc import abstractmethod


class ARMControllerABC(ControllerInterface):
    controller = None

    def get_phys_dict(self, *args, **kwargs):
        """ Получить состояние входов или выходов с контроллера.
        Перед возвратом привести в вид словаря,
        где ключ - это номер реле или di, значение - 0 или 1.
        """
        controller_response = self.get_controller_response()
        if "error" in controller_response:
            return controller_response
        response_dict = {i: x for i, x in enumerate(controller_response)}
        return response_dict

    @abstractmethod
    def get_controller_response(self):
        return []


class ARMK210ControllerDI(ARMControllerABC):
    map_keys_amount = 8
    starts_with = 0

    def __init__(self, controller):
        self.controller = controller

    def get_controller_response(self):
        response = self.controller.read_input_registers(
            self.starts_with, self.map_keys_amount)
        if not response:
            response = {"error": "None response from controller"}
        return response


class ARMK210ControllerRelay(ARMControllerABC):
    map_keys_amount = 8
    starts_with = 0

    def __init__(self, controller):
        self.controller = controller

    def get_controller_response(self):
        response = self.controller.read_holding_registers(
            self.starts_with, self.map_keys_amount)
        if not response:
            response = {"error": "None response from controller"}
        return response


class ARMK210Controller:
    def __init__(self, ip: str, port: int = 8234, name="ARM_K210_Controller"):
        self.controller = ModbusClient(host=ip, port=port)
        self.relay_interface = ARMK210ControllerRelay(self.controller)
        self.di_interface = ARMK210ControllerDI(self.controller)


