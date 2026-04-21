import rclpy
from rclpy.node import Node

from my_uvms_drivers.arm_joint_interface import ArmJointInterface
from my_uvms_drivers.rov_reference_interface import ROVReferenceInterface


class AUVArmGraspController(Node):
    """Simple staged demo controller using the existing Blue and Reach low-level wrappers."""

    def __init__(self):
        super().__init__('auv_arm_grasp_controller')
        self.rov = ROVReferenceInterface(self)
        self.arm = ArmJointInterface(self)
        self.step = 0
        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info('UVMS staged grasp controller started.')

    def control_loop(self):
        if self.step < 30:
            self.rov.command(surge=0.08)
        elif self.step == 30:
            self.rov.stop()
            self.arm.command_all(0.0, 0.2, 0.3, 1.4, 0.1)
        elif self.step == 60:
            self.arm.command_jaw(0.01)
        elif self.step == 90:
            self.arm.command_all(0.01, 0.0, 0.0, 1.2, 0.0)
            self.rov.command(surge=-0.05)
        elif self.step > 120:
            self.rov.stop()
            self.timer.cancel()
            self.get_logger().info('Demo sequence complete.')
            return
        self.step += 1


def main(args=None):
    rclpy.init(args=args)
    node = AUVArmGraspController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
