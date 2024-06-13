import math


class ActionNed:
    def __init__(self, robot_object):
        self.robot_object = robot_object

    def move_joints(self, j1, j2, j3, j4, j5, j6):
        trans = math.pi / 180
        self.robot_object.move_joints(j1 * trans, j2 * trans, j3 * trans, j4 * trans, j5 * trans, j6 * trans)

    def get_joints(self):
        joints_rad = self.robot_object.get_joints()
        joints_degrees = [round(joint * 180 / math.pi, 3) for joint in joints_rad]
        return joints_degrees

    def move_cartesian(self, x, y, z, roll, pitch, yaw):
        trans = math.pi / 180
        self.robot_object.move_pose(x, y, z, roll * trans, pitch * trans, yaw * trans)

    def get_cartesian(self):
        return self.robot_object.get_pose()

    def move_to_home(self):
        self.robot_object.move_to_home_pose()

    def move_to_zero(self):
        self.robot_object.move_joints([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    def open_gripper(self):
        self.robot_object.release_with_tool()

    def close_gripper(self):
        self.robot_object.grasp_with_tool()

    def set_velocity(self, velocity):
        self.robot_object.set_arm_max_velocity(velocity)

    def calibrate(self):
        self.robot_object.calibrate_auto()

    def go_to_sleep(self):
        self.robot_object.go_to_sleep()

    def apply_emergency_stop(self):
        ...
