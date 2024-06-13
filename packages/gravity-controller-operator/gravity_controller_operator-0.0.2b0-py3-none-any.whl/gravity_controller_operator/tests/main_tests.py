import unittest
from gravity_controller_operator.controllers.arm_k210 import ARMK210Controller


class TestCase(unittest.TestCase):
    def test_relay_controller(self):
        controller = ARMK210Controller(ip="127.0.0.1")
        state = controller.relay_interface.get_phys_dict()
        print(state)


if __name__ == "__main__":
    unittest.main()
