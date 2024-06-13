from pyniryo import *


class ConnectNed:
    def __init__(self):
        self.robot_object = None

    def connect_robot(self, ip_address):
        self.robot_object = NiryoRobot(ip_address)
        self.robot_object.calibrate_auto()
        return self.robot_object

    def disconnect_robot(self):
        self.robot_object.close_connection()
