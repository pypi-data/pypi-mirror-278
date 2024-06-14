from gravity_controller_operator.controllers_super import ControllerInterface, \
    RelayControllerInterface
from pyModbusTCP.client import ModbusClient
from abc import abstractmethod


class ARMControllerABC(ControllerInterface):
    controller = None

    def get_phys_dict(self, *args, **kwargs):
        """ Получить состояние входов или выходов с контроллера.
        Перед возвратом привести в вид словаря,
        где ключ - это номер реле или di, значение - 0 или 1.
        """
        controller_response = self.get_phys_points_states()
        if "error" in controller_response:
            return controller_response
        response_dict = {i: x for i, x in enumerate(controller_response)}
        return response_dict

    @abstractmethod
    def get_phys_points_states(self):
        return []


class ARMK210ControllerDI(ARMControllerABC):
    map_keys_amount = 8
    starts_with = 0

    def __init__(self, controller):
        self.controller = controller
        self.init_dict()
        self.update_dict()

    def get_phys_points_states(self):
        response = self.controller.read_input_registers(
            self.starts_with, self.map_keys_amount)
        if not response:
            response = {"error": "None response from controller"}
        return response


class ARMK210ControllerRelay(ARMControllerABC, RelayControllerInterface):
    map_keys_amount = 8
    starts_with = 0

    def __init__(self, controller):
        self.controller = controller
        self.init_dict()
        self.update_dict()

    def get_phys_points_states(self):
        response = self.controller.read_holding_registers(
            self.starts_with, self.map_keys_amount)
        if not response:
            response = {"error": "None response from controller"}
        return response

    def change_phys_relay_state(self, num, state: bool):
        self.controller.write_single_coil(num, state)


class ARMK210Controller:
    model = "arm_k210"

    def __init__(self, ip: str, port: int = 8234, name="ARM_K210_Controller"):
        self.controller_interface = ModbusClient(host=ip, port=port)
        self.relay_interface = ARMK210ControllerRelay(
            self.controller_interface)
        self.di_interface = ARMK210ControllerDI(
            self.controller_interface)


