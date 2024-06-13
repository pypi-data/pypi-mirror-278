from kortex_api.autogen.messages import Base_pb2
import threading
import time

TIMEOUT_DURATION = 10


# Classe de movimentação adaptada dos exemplos disponibilizados pela API.
# Essa classe é a única (até agora) que tem contato direto com a base (CPU) do Gen3
class Gen3Api:
    @staticmethod
    def check_for_end_or_abort(error):
        def check(notification, e=error):
            if notification.action_event == Base_pb2.ACTION_END or notification.action_event == Base_pb2.ACTION_ABORT:
                e.set()

        return check

    def move_to_home(self, base):
        # Make sure the arm is in Single Level Servoing mode
        base_servo_mode = Base_pb2.ServoingModeInformation()
        base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
        base.SetServoingMode(base_servo_mode)

        # Move arm to ready position
        action_type = Base_pb2.RequestedActionType()
        action_type.action_type = Base_pb2.REACH_JOINT_ANGLES
        action_list = base.ReadAllActions(action_type)
        action_handle = None
        for action in action_list.action_list:
            if action.name == "Home":
                action_handle = action.handle

        if action_handle is None:
            print("Can't reach safe position. Exiting")
            return False

        e = threading.Event()
        notification_handle = base.OnNotificationActionTopic(
            self.check_for_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )

        base.ExecuteActionFromReference(action_handle)
        finished = e.wait(TIMEOUT_DURATION)
        base.Unsubscribe(notification_handle)

        if finished:
            print("Safe position reached")
        else:
            print("Timeout on action notification wait")
        return finished

    @staticmethod
    def populate_angular_pose(joint_pose, duration_factor):
        waypoint = Base_pb2.AngularWaypoint()
        waypoint.angles.extend(joint_pose)
        waypoint.duration = duration_factor * 5.0

        return waypoint

    # Método utilizado para mover o robô para waypoints definidos.
    def move_trajectory(self, base, joints_list):
        base_servo_mode = Base_pb2.ServoingModeInformation()
        base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
        base.SetServoingMode(base_servo_mode)

        joint_poses = joints_list

        waypoints = Base_pb2.WaypointList()
        waypoints.duration = 0.0
        waypoints.use_optimal_blending = False

        index = 0
        for joint_pose in joint_poses:
            waypoint = waypoints.waypoints.add()
            waypoint.name = "waypoint_" + str(index)
            duration_factor = 1
            # Joints/motors 5 and 7 are slower and need more time
            if index == 4 or index == 6:
                duration_factor = 6  # Min 30 seconds

            waypoint.angular_waypoint.CopyFrom(self.populate_angular_pose(joint_pose, duration_factor))
            index = index + 1

            # Verify validity of waypoints
        result = base.ValidateWaypointList(waypoints)
        if len(result.trajectory_error_report.trajectory_error_elements) == 0:

            e = threading.Event()
            notification_handle = base.OnNotificationActionTopic(
                self.check_for_end_or_abort(e),
                Base_pb2.NotificationOptions()
            )

            base.ExecuteWaypointTrajectory(waypoints)

            finished = e.wait(TIMEOUT_DURATION)
            base.Unsubscribe(notification_handle)

            if finished:
                pass
            else:
                print("Timeout on action notification wait")
            return finished
        else:
            pass

    # O método move_joints chama esse método para mover as juntas.
    def angular_movement(self, base, joints_list):
        # Starting angular action movement
        action = Base_pb2.Action()
        action.name = "Angular action movement"
        action.application_data = ""

        # Place arm straight up
        joint_id = 1
        for joint_value in joints_list:
            joint_angle = action.reach_joint_angles.joint_angles.joint_angles.add()
            joint_angle.joint_identifier = joint_id
            joint_angle.value = joint_value
            joint_id += 1

        e = threading.Event()
        notification_handle = base.OnNotificationActionTopic(
            self.check_for_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )

        # Executing action
        base.ExecuteAction(action)

        # Waiting for movement to finish
        finished = e.wait(TIMEOUT_DURATION)
        base.Unsubscribe(notification_handle)

        if finished:
            pass
        else:
            print("Timeout on action notification wait")
        return finished

    def cartesian_movement(self, base, cartesian_list):
        # Starting Cartesian action movement
        action = Base_pb2.Action()
        action.name = "Example Cartesian action movement"
        action.application_data = ""

        cartesian_pose = action.reach_pose.target_pose
        cartesian_pose.x = cartesian_list[0]  # (meters)
        cartesian_pose.y = cartesian_list[1]  # (meters)
        cartesian_pose.z = cartesian_list[2]  # (meters)
        cartesian_pose.theta_x = cartesian_list[3]  # (degrees)
        cartesian_pose.theta_y = cartesian_list[4]  # (degrees)
        cartesian_pose.theta_z = cartesian_list[5]  # (degrees)

        e = threading.Event()
        notification_handle = base.OnNotificationActionTopic(
            self.check_for_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )

        # Executing action
        base.ExecuteAction(action)

        # Waiting for movement to finish
        finished = e.wait(TIMEOUT_DURATION)
        base.Unsubscribe(notification_handle)

        if finished:
            pass
        else:
            print("Timeout on action notification wait")
        return finished

    # Função para fechar a garra. Ver outra opção ao sleep.
    @staticmethod
    def close_gripper(base, close_time):
        # Create the GripperCommand we will send
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()

        # Close the gripper with position increments
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        finger.value = 1
        base.SendGripperCommand(gripper_command)

        time.sleep(close_time)

    # Função para abrir a garra. Ver outra opção ao sleep.
    @staticmethod
    def open_gripper(base, open_time):
        # Create the GripperCommand we will send
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()

        # Close the gripper with position increments
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        finger.value = 0
        base.SendGripperCommand(gripper_command)

        time.sleep(open_time)

    @staticmethod
    def get_joints(base_cyclic):
        feedback = base_cyclic.RefreshFeedback()
        joints = [round(feedback.actuators[joint].position, 3) for joint in range(0, 6)]

        return joints

    @staticmethod
    def get_cartesian(base_cyclic):
        fb = base_cyclic.RefreshFeedback()
        pose_meters = [round(fb.base.tool_pose_x, 3), round(fb.base.tool_pose_y, 3), round(fb.base.tool_pose_z, 3),
                       round(fb.base.tool_pose_theta_x, 3), round(fb.base.tool_pose_theta_y, 3),
                       round(fb.base.tool_pose_theta_z, 3)]

        return pose_meters

    @staticmethod
    def set_velocity(base, velocity):
        ...

    @staticmethod
    def apply_emergency_stop(base):
        base.ApplyEmergencyStop()
