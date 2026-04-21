from std_msgs.msg import Float64MultiArray


class ArmJointInterface:
    """Publish Reach Alpha 5 joint-angle commands using the existing forward position controllers.

    The Alpha 5 stack splits the end-effector jaw (axis_a) and the main arm joints
    (axis_b..axis_e) into separate controllers. This wrapper exposes a single Python API
    and handles the split internally.
    """

    def __init__(
        self,
        node,
        arm_topic: str = '/forward_position_controller/commands',
        jaw_topic: str = '/tcp_position_controller/commands',
        queue_size: int = 10,
    ):
        self._arm_pub = node.create_publisher(Float64MultiArray, arm_topic, queue_size)
        self._jaw_pub = node.create_publisher(Float64MultiArray, jaw_topic, queue_size)
        self.arm_topic = arm_topic
        self.jaw_topic = jaw_topic

    def command_arm(self, axis_b: float, axis_c: float, axis_d: float, axis_e: float):
        msg = Float64MultiArray()
        msg.data = [float(axis_b), float(axis_c), float(axis_d), float(axis_e)]
        self._arm_pub.publish(msg)

    def command_jaw(self, axis_a: float):
        msg = Float64MultiArray()
        msg.data = [float(axis_a)]
        self._jaw_pub.publish(msg)

    def command_all(self, axis_a: float, axis_b: float, axis_c: float, axis_d: float, axis_e: float):
        self.command_jaw(axis_a)
        self.command_arm(axis_b, axis_c, axis_d, axis_e)
