import unittest
from gravity_controller_operator.controllers.arm_k210 import ARMK210Controller


class TestCase(unittest.TestCase):
    controller = ARMK210Controller(ip="127.0.0.1")

    def test_di_response(self):
        self.controller.di_interface.init_dict()
        self.controller.di_interface.update_dict()
        state = self.controller.di_interface.get_dict()
        self.assertDictEqual(
            state,
            {0: {'state': 0, 'changed': False},
             1: {'state': 0, 'changed': False},
             2: {'state': 0, 'changed': False},
             3: {'state': 0, 'changed': False},
             4: {'state': 1, 'changed': False},
             5: {'state': 0, 'changed': False},
             6: {'state': 0, 'changed': False},
             7: {'state': 0, 'changed': False}})

    def test_relay_change(self):
        relay_num = 1
        relay_interface = self.controller.relay_interface
        phys_states = relay_interface.get_phys_points_states()
        self.assertEqual(phys_states, [0, 0, 0, 0, 0, 0, 0, 0])
        relay_state = relay_interface.get_point_state(relay_num)
        self.assertEqual(relay_state, {"state": False, "changed": False})

        relay_interface.change_relay_state(relay_num, True)
        phys_states = relay_interface.get_phys_points_states()
        self.assertEqual(phys_states, [0, 1, 0, 0, 0, 0, 0, 0])
        relay_state = relay_interface.get_point_state(relay_num)
        self.assertEqual(relay_state["state"], True)
        relay_interface.change_relay_state(relay_num, False)

if __name__ == "__main__":
    unittest.main()
