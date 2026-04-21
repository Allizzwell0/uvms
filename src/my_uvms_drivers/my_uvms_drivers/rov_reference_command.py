import argparse

import rclpy
from rclpy.node import Node

from my_uvms_drivers.rov_reference_interface import ROVReferenceInterface


class _CmdNode(Node):
    def __init__(self, args):
        super().__init__('rov_reference_command')
        self.iface = ROVReferenceInterface(self)
        self.iface.command(
            surge=args.surge,
            sway=args.sway,
            heave=args.heave,
            roll_rate=args.roll_rate,
            pitch_rate=args.pitch_rate,
            yaw_rate=args.yaw_rate,
        )
        self.get_logger().info(f'Published ROV reference on {self.iface.topic}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--surge', type=float, default=0.0)
    parser.add_argument('--sway', type=float, default=0.0)
    parser.add_argument('--heave', type=float, default=0.0)
    parser.add_argument('--roll-rate', type=float, default=0.0)
    parser.add_argument('--pitch-rate', type=float, default=0.0)
    parser.add_argument('--yaw-rate', type=float, default=0.0)
    args = parser.parse_args()

    rclpy.init()
    node = _CmdNode(args)
    rclpy.spin_once(node, timeout_sec=0.1)
    node.destroy_node()
    rclpy.shutdown()
