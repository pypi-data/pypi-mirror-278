from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient
from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from rria_api.gen3.api_gen3.gen3_api import Gen3Api


class ActionGen3:
    def __init__(self, route):
        self.route = route
        self.base = BaseClient(self.route)
        self.base_cyclic = BaseCyclicClient(self.route)

    def move_joints(self, joints_list):
        Gen3Api().angular_movement(self.base, joints_list)

    def get_joints(self):
        return Gen3Api().get_joints(self.base_cyclic)

    def move_cartesian(self, cartesian_list):
        Gen3Api().cartesian_movement(self.base, cartesian_list)

    def get_cartesian(self):
        return Gen3Api().get_cartesian(self.base_cyclic)

    def move_to_home(self):
        Gen3Api().move_to_home(self.base)

    def move_to_zero(self):
        joints_list = [0, 0, 0, 0, 0, 0]
        Gen3Api().angular_movement(self.base, joints_list)

    def open_gripper(self, execution_time):
        Gen3Api().open_gripper(self.base, execution_time)

    def close_gripper(self, execution_time):
        Gen3Api().close_gripper(self.base, execution_time)

    def set_velocity(self, velocity):
        Gen3Api().set_velocity(self.base, velocity)

    def calibrate(self):
        ...

    def go_to_sleep(self):
        joints_list = [0.0, 26, 149.9, 0.0, 0.0, 0.0]
        Gen3Api().angular_movement(self.base, joints_list)

    def apply_emergency_stop(self):
        Gen3Api().apply_emergency_stop(self.base)
