from rria_api.ned.connect_ned import ConnectNed
from rria_api.ned.action_ned import ActionNed
from rria_api.gen3.connect_gen3 import ConnectGen3
from rria_api.gen3.action_gen3 import ActionGen3
from rria_api.robot_enum import RobotEnum
from time import sleep


class RobotObject:
    def __init__(self, ip_address, robot_type):
        """
        This class is used to initialize and use the robot object.
        :param ip_address: string with the ip address of the robot
        :param robot_type: enum with the type of the robot
        """
        self.ip_address = ip_address
        self.robot_type = robot_type

        # This atribute is used to store the general robot instance
        self.robot_instance = None

        # This atribute is used to store the general connection instance
        self.connection_instance = None

    def connect_robot(self) -> bool:
        """
        Connect robot depends on the robot type
        :rtype: bool

        """

        if self.robot_type is RobotEnum.GEN3_LITE:
            try:
                self.connection_instance = ConnectGen3(self.ip_address, ["admin", "admin"])
                self.robot_instance = self.connection_instance.connect_robot()

                return True

            except(Exception,):
                print('The connection attempt failed. Check the physical connection to the robot and try again later.')

                return False

        if self.robot_type is RobotEnum.NED:
            try:
                self.connection_instance = ConnectNed()
                self.robot_instance = self.connection_instance.connect_robot(self.ip_address)

                return True

            except(Exception,):
                print('The connection attempt failed. Check the physical connection to the robot and try again later.')

                return False

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return True

    def disconnect_robot(self):
        """
        Close connection with robot
        :rtype: None

        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            self.connection_instance.disconnect_robot()

        if self.robot_type is RobotEnum.NED:
            self.connection_instance.disconnect_robot()

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return True

    def safe_disconnect(self):
        """
        Move robot for home position and close connection with robot. Home position dependes on robot type. For Gen3 is
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] degrees and for Ned is [0.0, 0.3, -1.3, 0.0, 0.0, 0.0] radians.
        :rtype: None

        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            ActionGen3(self.robot_instance).go_to_sleep()
            self.connection_instance.disconnect_robot()

        if self.robot_type is RobotEnum.NED:
            ActionNed(self.robot_instance).move_to_home()
            self.connection_instance.disconnect_robot()

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return True

    # Move Joints/Cartesian methods
    @property
    def joints(self) -> list:
        return self.get_joints()

    def get_joints(self) -> list:
        """
        Get joints value in degrees
        You can also use a getter ::

            joints = robot.get_joints()
            joints = robot.joints

        :return: List of joints value
        :rtype: list[float]
        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            return ActionGen3(self.robot_instance).get_joints()

        if self.robot_type is RobotEnum.NED:
            return ActionNed(self.robot_instance).get_joints()

        if self.robot_type is RobotEnum.DUMMY:
            sleep(0.5)
            return ['J1', 'J2', 'J3', 'J4', 'J5', 'J6']

    def move_joints(self, j1, j2, j3, j4, j5, j6):
        """
        Move robot joints. Joints are expressed in degrees.

        All lines of the next example realize the same operation: ::

            robot.move_joints(0.2, 0.1, 0.3, 0.0, 0.5, 0.0)

        :param j1: joint 1,
        :type j1: float
        :param j2: joint 2,
        :type j2: float
        :param j3: joint 3,
        :type j3: float
        :param j4: joint 4,
        :type j4: float
        :param j5: joint 5,
        :type j5: float
        :param j6: joint 6,
        :type j6: float
        :rtype: None
        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            ActionGen3(self.robot_instance).move_joints([j1, j2, j3, j4, j5, j6])

        if self.robot_type is RobotEnum.NED:
            ActionNed(self.robot_instance).move_joints(j1, j2, j3, j4, j5, j6)

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return True

    @property
    def cartesian(self) -> list:
        """
        Get an end-effector link as [x, y, z, roll, pitch, yaw].
        Call this method is equivalent to call get_cartesian() method.

        :return: Robot pose list.
        :rtype: list[float]
        """
        return self.get_cartesian()

    def get_cartesian(self) -> list:
        """
        Get an end-effector link pose as [x, y, z, roll, pitch, yaw].
        x, y & z are expressed in meters / roll, pitch & yaw are expressed in degrees from Gen3 Lite
        and radians from Ned.
        You can also use a getter ::

            joints = robot.get_cartesian()
            joints = robot.cartesian

        :return: Robot pose list.
        :rtype: list[float]
        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            return ActionGen3(self.robot_instance).get_cartesian()

        if self.robot_type is RobotEnum.NED:
            return ActionNed(self.robot_instance).get_cartesian()

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return ['x', 'y', 'z', 'roll', 'pitch', 'yaw']

    def move_cartesian(self, x, y, z, roll, pitch, yaw):
        """
        Move robot end effector pose to a (x, y, z, roll, pitch, yaw, frame_name) pose
        in a particular frame (frame_name) if defined.
        x, y & z are expressed in meters / roll, pitch & yaw are expressed in degrees.

        All lines of the next example realize the same operation: ::

            robot.move_cartesian(0.2, 0.1, 0.3, 0.0, 0.5, 0.0)

        :param x: coordinate x,
        :type x: float
        :param y: coordinate y,
        :type y: float
        :param z: coordinate z,
        :type z: float
        :param roll: rotation on x-axis,
        :type roll: float
        :param pitch: rotation on y-axis,
        :type pitch: float
        :param yaw: rotation on z-axis,
        :type yaw: float
        :rtype: None
        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            return ActionGen3(self.robot_instance).move_cartesian([x, y, z, roll, pitch, yaw])

        if self.robot_type is RobotEnum.NED:
            return ActionNed(self.robot_instance).move_cartesian(x, y, z, roll, pitch, yaw)

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return True

    # TODO: Pegar os valores de home do robot
    def move_to_home(self):
        """
        Move robot for home position. Home position dependes on robot type. For Gen3 is [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        degrees and for Ned is [0.0, 0.3, -1.3, 0.0, 0.0, 0.0] radians.

        :rtype: None
        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            ActionGen3(self.robot_instance).move_to_home()

        if self.robot_type is RobotEnum.NED:
            ActionNed(self.robot_instance).move_to_home()

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return True

    def move_to_zero(self):
        """
        Move robot for zero position. Home position dependes on robot type. For Gen3 is [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        degrees and for Ned is [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] degrees.

        :rtype: None
        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            ActionGen3(self.robot_instance).move_to_zero()

        if self.robot_type is RobotEnum.NED:
            ActionNed(self.robot_instance).move_to_zero()

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return True

    def open_gripper(self, actuation_time=2):
        """
        Fully open gripper.
        :param (optional) actuation_time: If gen3_lite is being used, it is possible to control the motor actuation time,
        to be able to partially open the gripper
        :rtype: None
        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            ActionGen3(self.robot_instance).open_gripper(actuation_time)

        if self.robot_type is RobotEnum.NED:
            ActionNed(self.robot_instance).open_gripper()

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return True

    def close_gripper(self, actuation_time=2):
        """
        Fully close gripper. 
        :param (optional) actuation_time: If gen3_lite is being used, it is possible to control the motor actuation time,
        to be able to partially close the gripper
        :rtype: None
        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            ActionGen3(self.robot_instance).close_gripper(actuation_time)

        if self.robot_type is RobotEnum.NED:
            ActionNed(self.robot_instance).close_gripper()

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return True

    # TODO: Ver a função de aumento de velocidade para o Gen3
    def set_velocity(self, velocity):
        """
        Limit arm max velocity to a percentage of its maximum velocity. For Niryo one, velocity is a percentage of 100.
        For gen3, there are two types of velocities, an angular and a cartesian. The speed used in this method is
        angular.

        :param velocity: Should be between 1 & 100 for niryo
        :type velocity: int
        :rtype: None
        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            ActionGen3(self.robot_instance).set_velocity(velocity)

        if self.robot_type is RobotEnum.NED:
            ActionNed(self.robot_instance).set_velocity(velocity)

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return True

    def calibrate(self):
        """
        Start an automatic motors calibration if motors are not calibrated yet

        :rtype: None
        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            print('Gen3 NÃO necessita de calibração')

        if self.robot_type is RobotEnum.NED:
            ActionNed(self.robot_instance).calibrate()

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return True

    def go_to_sleep(self):
        """
        Go home pose and activate learning mode. The function is available only for Ned robot.

        :rtype: None
        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            ActionGen3(self.robot_instance).go_to_sleep()

        if self.robot_type is RobotEnum.NED:
            ActionNed(self.robot_instance).go_to_sleep()

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return True

    def apply_emergency_stop(self):
        """
        Apply emergency stop. The function is available only for Kinova Gen3.

        :rtype: None
        """
        if self.robot_type is RobotEnum.GEN3_LITE:
            ActionGen3(self.robot_instance).apply_emergency_stop()

        if self.robot_type is RobotEnum.NED:
            ...

        if self.robot_type is RobotEnum.DUMMY:
            sleep(1)
            return True
