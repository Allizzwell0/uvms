import argparse

import rclpy
from rclpy.node import Node

from my_uvms_drivers.arm_joint_interface import ArmJointInterface


class _CmdNode(Node):
    def __init__(self, args):
        super().__init__('arm_joint_command')
        self.iface = ArmJointInterface(self)
        self.iface.command_all(args.axis_a, args.axis_b, args.axis_c, args.axis_d, args.axis_e)
        self.get_logger().info(
            f'Published arm commands on {self.iface.arm_topic} and jaw command on {self.iface.jaw_topic}'
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--axis-a', type=float, default=0.0)
    parser.add_argument('--axis-b', type=float, default=0.0)
    parser.add_argument('--axis-c', type=float, default=0.0)
    parser.add_argument('--axis-d', type=float, default=1.5746)
    parser.add_argument('--axis-e', type=float, default=0.0)
    args = parser.parse_args()

    rclpy.init()
    node = _CmdNode(args)
    rclpy.spin_once(node, timeout_sec=0.1)
    node.destroy_node()
    rclpy.shutdown()
